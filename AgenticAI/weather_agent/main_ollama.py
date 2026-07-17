"""
Prereq: Ollama running (ollama serve) with model pulled.
"""

from openai import OpenAI
from dotenv import load_dotenv
import os
import json
import requests
from pydantic import BaseModel, Field, ValidationError, model_validator
from typing import Optional, Literal

load_dotenv()

OLLAMA_BASE_URL = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434/v1")
OLLAMA_MODEL = os.getenv("OLLAMA_MODEL", "gemma2:2b")

client = OpenAI(
    api_key="ollama",
    base_url=OLLAMA_BASE_URL,
)


def run_commnd(cmd: str):
    result = os.system(cmd)
    return result


def get_weather(city: str):
    url = f"https://wttr.in/{city}?format=%c+%t"
    headers = {"User-Agent": "curl/7.64.1"}
    try:
        res = requests.get(url, headers=headers, timeout=10)
    except requests.RequestException as e:
        return f"Weather service unavailable: {e}"
    print(city, res.status_code, "res get_weather")
    if res.status_code == 200:
        return f"The weather in {city} is {res.text}"

    else:
        return f"Could not find weather for {city}"


available_tools = {"get_weather": get_weather, "run_commnd": run_commnd}

SYSTEM_PROMPT = """
You are a helpful AI assistant named Brody. You can answer general questions and use tools when needed.
Pick the right tool for each task.

You MUST respond with a single valid JSON object only. No markdown, no code fences, no extra text.
Required keys: "step", "content". For tool steps also include "available_tool" and "tool_input".

Return only the NEXT step. Never return multiple steps in one message.
Never repeat the same step twice. After think, the next response MUST be plan. After plan, MUST be tool.

Follow steps in order across multiple turns:

STEP 1 - think: Understand what the user is asking and break it down.
STEP 2 - plan: Decide the best approach and which tool to use (get_weather or run_commnd).
STEP 3 - tool: Call the tool. Set available_tool and tool_input. Leave content empty or brief.
STEP 4 - output: Give the final answer using the observe result from conversation history.

After you send a tool step, STOP and wait. The system runs the tool and injects an observe message with real output.
Do NOT generate observe yourself. Never invent tool output or fake command results.

Available tools:
- get_weather(city: str): Use ONLY for weather questions. tool_input is the city name.
- run_commnd(cmd: str): Use for shell tasks (mkdir, ls, pwd, etc.). tool_input is the full Linux command.
  The user runs WSL/Linux — use Linux syntax (mkdir -p, ls, not PowerShell commands).


Tool selection:
- Weather question → get_weather
- Create folder, list files, run shell command → run_commnd
- General knowledge with no tool needed → still follow think/plan; use run_commnd only if a command is required

Example 1 — weather:

USER: What is the weather in Palampur?

ASSISTANT: {"step": "think", "content": "The user wants current weather for Palampur."}

ASSISTANT: {"step": "plan", "content": "I will use get_weather with Palampur as the city."}

ASSISTANT: {"step": "tool", "available_tool": "get_weather", "tool_input": "Palampur", "content": ""}

(System injects observe with real tool output — you do not write this step.)

ASSISTANT: {"step": "output", "content": "Based on the tool result, here is the current weather in Palampur: ..."}

Example 2 — create folder:

USER: Create a folder named todo_app in the AgenticAI directory.

ASSISTANT: {"step": "think", "content": "The user wants a new folder todo_app in AgenticAI."}

ASSISTANT: {"step": "plan", "content": "I will use run_commnd with mkdir from the parent directory."}

ASSISTANT: {"step": "tool", "available_tool": "run_commnd", "tool_input": "mkdir -p ../todo_app", "content": ""}

(System injects observe — you do not write this step.)

ASSISTANT: {"step": "output", "content": "The folder todo_app was created in the AgenticAI directory."}

Rules:
- The "content" field must ALWAYS be a plain string. Never return nested JSON inside content.
- For tool steps, available_tool and tool_input are required.
- Complete think, plan, tool, then output across separate responses.
- Keep think and plan concise. Put the user-facing answer in output.
- Use only real results from observe in output. Never make up data or command output.
"""


class OutputFormat(BaseModel):
    step: Literal["think", "plan", "tool", "output"]
    content: Optional[str] = Field(
        default=None,
        description="Assistant text for this step. Use empty string for tool step.",
    )
    available_tool: Optional[str] = Field(
        default=None, description="Tool name when step is 'tool'."
    )
    tool_input: Optional[str] = Field(
        default=None, description="Tool argument when step is 'tool'."
    )

    @model_validator(mode="after")
    def tool_has_tool_fields(self):
        if self.step in ("think", "plan", "output") and not self.content:
            raise ValueError(f"{self.step} step requires content")
        if self.step == "tool":
            if not self.available_tool or not self.tool_input:
                raise ValueError("tool step requires available_tool and tool_input")
        return self


def main(user_input):

    message_history = [
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "user", "content": user_input},
    ]

    while True:
        res = client.chat.completions.create(
            model=OLLAMA_MODEL,
            messages=message_history,
            response_format={"type": "json_object"},
        )

        raw_res = res.choices[0].message.content
        message_history.append({"role": "assistant", "content": raw_res})

        try:
            parsed_res = OutputFormat.model_validate(json.loads(raw_res))
        except (json.JSONDecodeError, ValidationError) as e:
            print(f"⚠️ Could not parse response: {raw_res}\n{e}")
            break

        if parsed_res.step == "think":
            print(f"🔥 {parsed_res.content}")
            continue

        if parsed_res.step == "plan":
            print(f"🧠 {parsed_res.content}")
            continue

        if parsed_res.step == "tool":
            tool_parsed = parsed_res.available_tool
            input_parsed = parsed_res.tool_input

            if tool_parsed not in available_tools:
                res_tool = f"Unknown tool: {tool_parsed}"
                print(f"🔧 {res_tool}")
            else:
                res_tool = available_tools[tool_parsed](input_parsed)
                print(f"🔧 {tool_parsed}, {input_parsed} = {res_tool}")

            message_history.append(
                {
                    "role": "user",
                    "content": json.dumps(
                        {
                            "step": "observe",
                            "available_tool": tool_parsed,
                            "tool_input": input_parsed,
                            "output": res_tool,
                        }
                    ),
                }
            )
            continue

        if parsed_res.step == "output":
            print(f"🤖 {parsed_res.content}")
            break


if __name__ == "__main__":
    print(f"Using Ollama model: {OLLAMA_MODEL} at {OLLAMA_BASE_URL}\n")

    while True:
        print("\n")

        user_input = input("👉 ")

        if user_input.strip().lower() == "q" or user_input.strip() == "":
            break

        main(user_input)

        print("\n")
