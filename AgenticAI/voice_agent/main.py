import speech_recognition as sr
from langchain.chat_models import init_chat_model
from langchain.agents import create_agent
from langgraph.checkpoint.memory import InMemorySaver
from dotenv import load_dotenv
from openai import AsyncOpenAI
from openai.helpers import LocalAudioPlayer
import asyncio

load_dotenv()

ASSISTANT_NAME = "Nova"

recognizer = sr.Recognizer()
llm_client = init_chat_model(model_provider="openai", model="gpt-4.1-mini")
async_opnai_client = AsyncOpenAI()

SYSTEM_PROMPT = f"""
You are {ASSISTANT_NAME}, a helpful voice assistant.

Context:
- User input comes from speech-to-text (may contain typos, missing punctuation, or misheard words).

Rules:
- Reply in plain spoken language only (no markdown, bullets, code blocks, or special symbols).
- Keep answers short: 1 to 3 sentences unless the user asks for more detail.
- Prefer clear, natural phrasing that is easy to hear.
- If the user's request is unclear or likely a STT error, ask one short clarifying question.
- Do not mention that you are an AI, STT, or TTS unless asked.
- Never claim to be Siri, Alexa, Gemini, or any other branded assistant.
"""

config = {"configurable": {"thread_id": "vipulbhardwaj"}}

agent = create_agent(
    model=llm_client,
    tools=[],
    system_prompt=SYSTEM_PROMPT,
    checkpointer=InMemorySaver(),
)


async def tts_openai(speech_txt: str):
    async with async_opnai_client.audio.speech.with_streaming_response.create(
        model="gpt-4o-mini-tts",
        voice="nova",
        input=speech_txt,
        instructions="Speak in a cheerful and positive tone.",
        response_format="pcm",
    ) as response:
        await LocalAudioPlayer().play(response)


def run_langchain_agent(input_txt: str) -> str:
    res = agent.invoke(
        {"messages": [{"role": "user", "content": input_txt}]},
        config=config,
    )
    return res["messages"][-1].content


def main():
    with sr.Microphone() as source:
        print("Calibrating mic (stay quiet for ~1s)...")
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

            print("Processing audio...")

            try:
                stt_google = recognizer.recognize_google(audio)
            except sr.UnknownValueError:
                print("Could not understand audio, try again...")
                continue
            except sr.RequestError as e:
                print("STT request failed:", e)
                continue

            print("Your speech to text: ", stt_google)

            if stt_google.strip().lower() in {"quit", "stop", "exit", "bye"}:
                print(f"Goodbye from {ASSISTANT_NAME}.")
                break

            agent_reply = run_langchain_agent(stt_google)
            print("agent_reply: ", agent_reply)
            asyncio.run(tts_openai(agent_reply))


if __name__ == "__main__":
    main()
