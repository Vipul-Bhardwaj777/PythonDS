"""
Nova — chained voice coding assistant (mic → OpenAI transcribe → agent → TTS).

Uses one asyncio event loop for STT/TTS; SpeechRecognition only captures the mic.
"""

from __future__ import annotations

import asyncio
import io
import json
import os
import re
import subprocess

import speech_recognition as sr
from dotenv import load_dotenv
from langchain.agents import create_agent
from langchain.chat_models import init_chat_model
from langchain.tools import tool
from langgraph.checkpoint.memory import InMemorySaver
from openai import AsyncOpenAI
from openai.helpers import LocalAudioPlayer

load_dotenv()

TRANSCRIBE_MODEL = "gpt-4o-mini-transcribe"
TTS_MODEL = "gpt-4o-mini-tts"


@tool
def run_command(cmd: str) -> str:
    """Run a shell command (mkdir, dir, cd, etc.). This machine is Windows — do not use Linux-only flags like mkdir -p or ls."""
    m = re.match(r"^mkdir\s+(?:-p\s+)?(.+)$", cmd.strip(), re.IGNORECASE)
    if m:
        path = m.group(1).strip().strip('"').strip("'")
        os.makedirs(path, exist_ok=True)
        return f"Created directory {path} (exit 0)"

    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    output = ((result.stdout or "") + (result.stderr or "")).strip()
    return f"exit={result.returncode}" + (f"\n{output}" if output else "")


@tool
def write_file(path: str, content: str) -> str:
    """Write or overwrite a file. Use for creating/editing code files."""
    parent = os.path.dirname(path)
    if parent:
        os.makedirs(parent, exist_ok=True)

    with open(path, "w", encoding="utf-8") as f:
        f.write(content)

    return f"Wrote {len(content)} bytes to {path}"


SYSTEM_PROMPT = """
You are Nova, a helpful voice coding assistant.
Your name is Nova — when the user greets you (hi Nova, hey Nova, etc.), greet them back warmly by name if you know it, or simply as Nova.
User input comes from speech-to-text (may have typos or misheard words).
Use tools when needed. Prefer tools over guessing for files and shell tasks.
You are on Windows: for new folders prefer write_file (it creates parent dirs), or mkdir without -p.
Reply in plain spoken language: short, clear, no markdown or code blocks unless the user asks.
Keep final answers to 1-3 sentences when speaking a summary after tools run.
"""

tools = [run_command, write_file]

llm = init_chat_model(model="gpt-4.1", model_provider="openai")
config = {"configurable": {"thread_id": "nova"}}

agent = create_agent(
    model=llm,
    tools=tools,
    system_prompt=SYSTEM_PROMPT,
    checkpointer=InMemorySaver(),
)

openai_async_client = AsyncOpenAI()
recognizer = sr.Recognizer()


async def stt_openai(audio: sr.AudioData) -> str:
    """Transcribe mic audio with OpenAI (wav in-memory)."""
    buf = io.BytesIO(audio.get_wav_data())
    buf.name = "speech.wav"
    transcription = await openai_async_client.audio.transcriptions.create(
        model=TRANSCRIBE_MODEL,
        file=buf,
    )
    return (transcription.text or "").strip()


async def tts_openai(speech: str) -> None:
    async with openai_async_client.audio.speech.with_streaming_response.create(
        model=TTS_MODEL,
        voice="nova",
        input=speech,
        instructions="Speak in a cheerful and positive tone.",
        response_format="pcm",
    ) as response:
        await LocalAudioPlayer().play(response)


def _print_messages(messages) -> None:
    for msg in messages:
        role = msg.type
        content = msg.content
        tool_calls = msg.tool_calls if role == "ai" else None

        if tool_calls:
            print(f"🤖 [{role}] tool_calls:")
            print(json.dumps(tool_calls, indent=2, default=str))
        else:
            preview = (
                content
                if isinstance(content, str)
                else json.dumps(content, default=str)
            )
            print(f"📨 [{role}] {preview}")


async def main() -> None:
    with sr.Microphone() as source:
        recognizer.adjust_for_ambient_noise(source, duration=1)
        recognizer.dynamic_energy_threshold = True
        recognizer.pause_threshold = 0.8
        recognizer.non_speaking_duration = 0.4

        while True:
            print("Speak something 🔊")

            try:

                audio = recognizer.listen(source, timeout=8, phrase_time_limit=10)
            except sr.WaitTimeoutError:
                print("No speech detected, try again...")
                continue

            try:
                user_text = await stt_openai(audio)
            except Exception as e:
                print("STT request failed:", e)
                continue

            if not user_text:
                print("Could not understand audio, try again...")
                continue

            print(f"You: {user_text}")

            if user_text.lower() in {"quit", "stop", "exit", "bye"}:
                print("Goodbye")
                break

            result = await agent.ainvoke(
                {"messages": [{"role": "user", "content": user_text}]},
                config=config,
            )

            _print_messages(result["messages"])

            text = result["messages"][-1].content
            if not isinstance(text, str):
                text = json.dumps(text, default=str)
            print(text)
            await tts_openai(text)


if __name__ == "__main__":
    asyncio.run(main())
