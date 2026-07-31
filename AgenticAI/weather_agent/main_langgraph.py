"""
Latest ReAct agent (LangChain 1.x) — compare with hand-rolled loop in main.py

main.py (hand-rolled):
  - You write the while-loop
  - You force think/plan/tool/output JSON steps
  - You manually run tools and inject "observe"

main_langgraph.py (latest):
  - create_agent builds the ReAct loop for you
  - Model uses native tool-calling (no custom step JSON)
  - Framework runs tools and feeds ToolMessage results back

Same tools, same idea: reason → act → observe → answer
"""

from __future__ import annotations

import json
import os

import requests
from dotenv import load_dotenv
from langchain.agents import create_agent
from langchain.tools import tool
from langchain.chat_models import init_chat_model

load_dotenv()


@tool
def get_weather(city: str) -> str:
    """Get current weather for a city. Use only for weather questions."""
    url = f"https://wttr.in/{city}?format=%c+%t"
    headers = {"User-Agent": "curl/7.64.1"}
    try:
        res = requests.get(url, headers=headers, timeout=10)
    except requests.RequestException as e:
        return f"Weather service unavailable: {e}"

    if res.status_code == 200:
        return f"The weather in {city} is {res.text}"
    return f"Could not find weather for {city}"


@tool
def run_commnd(cmd: str) -> str:
    """Run a shell command (mkdir, ls, pwd, etc.). Prefer Linux/WSL syntax."""
    exit_code = os.system(cmd)
    return f"Command finished with exit code {exit_code}"


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
You are a helpful AI assistant named Brody.
Use tools when needed. Prefer tools over guessing for weather, files, and shell tasks.
Keep final answers concise.
"""

# Same tools as main.py, but registered with @tool so the model can call them natively
tools = [get_weather, run_commnd, write_file]

llm = init_chat_model(model="gpt-4o-mini", model_provider="openai")

# This IS the ReAct loop — no while True / observe plumbing from you
agent = create_agent(
    model=llm,
    tools=tools,
    system_prompt=SYSTEM_PROMPT,
)


def main(user_input: str) -> None:
    result = agent.invoke(
        {"messages": [{"role": "user", "content": user_input}]},
    )

    for msg in result["messages"]:
        role = getattr(msg, "type", msg.__class__.__name__)
        content = getattr(msg, "content", "")

        tool_calls = getattr(msg, "tool_calls", None)
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

    final = result["messages"][-1]
    print(getattr(final, "content", final))


if __name__ == "__main__":
    while True:
        print("\n")
        user_input = input("👉 ")
        if user_input.strip().lower() == "q" or user_input.strip() == "":
            break
        main(user_input)
        print("\n")
