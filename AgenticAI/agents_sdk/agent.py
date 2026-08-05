from agents import Agent, Runner, WebSearchTool, function_tool, SQLiteSession

import asyncio

from dotenv import load_dotenv

import requests


load_dotenv()


@function_tool
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


SYSTEM_PROMPT = "You are a friendly chat bot"

agent = Agent(
    name="chat_bot",
    model="gpt-4.1-mini",
    instructions=SYSTEM_PROMPT,
    tools=[WebSearchTool(), get_weather],
    # output_type=AgentReplySchema        # using pydantic basemodel
)


async def main() -> None:

    user_session = SQLiteSession("vipul_chat")

    while True:

        print("\n")

        user_input = input("👉 ").strip()

        if not user_input or user_input.lower() == "q":

            break

        result = await Runner.run(agent, user_input, session=user_session)

        print(result.final_output)

        print("\n")


if __name__ == "__main__":

    asyncio.run(main())
