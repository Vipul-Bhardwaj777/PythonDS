from openai import OpenAI
from dotenv import load_dotenv
import os
import json
import requests

load_dotenv()

G_KEY = os.getenv("GEMINI_API_KEY")

client = OpenAI(
    api_key=G_KEY, base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
)


def get_weather(city: str):
    url = f"https://wttr.in/{city}?format=j1"
    headers = {"User-Agent": "curl/7.64.1"}
    res = requests.get(url, headers)

    if res.status_code == 200:
        current_weather = res.json()["current_condition"][0]
        desc = current_weather["weatherDesc"][0]["value"].strip()
        tempC = current_weather["temp_C"]
        return f"The weather in {city} is {desc} with {tempC}"

    else:
        return f"Could not find weather for {city}"


available_tools = {"get_weather": get_weather}

SYSTEM_PROMPT = """
You are a helpful AI assistant named Brody, specialized in weather questions.
You can call a tool from the available tools list when needed.

For every request respond ONLY in this JSON format, no extra text:
{
    "step": "think" | "plan" | "tool" | "output",
    "content": "your content here",
    "available_tool": "string",
    "input": "string"
}

IMPORTANT: Return exactly ONE JSON object per response.
Return only the NEXT step. Never return multiple steps in one message.

Follow steps in order across multiple turns:

STEP 1 - think: Understand what the user is asking and break it down.
STEP 2 - plan: Decide the best approach. If get_weather is needed, say so in one plan step.
STEP 3 - tool: Call the tool. Set available_tool and input. Leave content empty or brief.
STEP 4 - output: Give the final answer using the observe result from conversation history.

After you send a tool step, STOP and wait. The system runs the tool and injects an observe message with real output.
Do NOT generate observe yourself. Never invent tool output or weather numbers.

Available tools:
- get_weather(city: str): Takes city name as input string and returns weather info as a string.

Example conversation:

USER: What is the weather in Palampur?

ASSISTANT: {"step": "think", "content": "The user wants current weather for Palampur."}

ASSISTANT: {"step": "plan", "content": "I will use get_weather with Palampur as the city."}

ASSISTANT: {"step": "tool", "available_tool": "get_weather", "input": "Palampur", "content": ""}

(System injects observe with real tool output — you do not write this step.)

ASSISTANT: {"step": "output", "content": "Based on the tool result, here is the current weather in Palampur: ..."}

Rules:
- The "content" field must ALWAYS be a plain string. Never return nested JSON inside content.
- For tool steps, available_tool and input are required.
- Never answer questions outside your defined steps.
- Complete think, plan, tool, then output across separate responses.
- Keep think and plan concise. Put the user-facing answer in output.
- Use only real numbers from observe in output. Never make up weather data.
"""


def main(user_input):

    message_history = [
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "user", "content": user_input},
    ]

    while True:
        res = client.chat.completions.create(
            model="gemini-2.5-flash",
            messages=message_history,
            response_format={"type": "json_object"},
        )

        raw_res = res.choices[0].message.content
        message_history.append({"role": "assistant", "content": raw_res})
        parsed_res = json.loads(raw_res)

        if parsed_res.get("step") == "think":
            print(f"🔥 {parsed_res.get('content')}")
            continue

        if parsed_res.get("step") == "plan":
            print(f"🧠 {parsed_res.get('content')}")
            continue

        if parsed_res.get("step") == "tool":
            tool_parsed = parsed_res.get("available_tool")
            input_parsed = parsed_res.get("input")

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
                            "input": input_parsed,
                            "output": res_tool,
                        }
                    ),
                }
            )
            continue

        if parsed_res.get("step") == "output":
            print(f"🤖 {parsed_res.get('content')}")
            break


if __name__ == "__main__":

    while True:
        print("\n")

        user_input = input("👉 ")

        if user_input.strip().lower() == "q" or user_input.strip() == "":
            break

        main(user_input)

        print("\n")
