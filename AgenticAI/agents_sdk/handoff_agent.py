from agents import Agent, Runner
from dotenv import load_dotenv
import asyncio

load_dotenv()

HISTORY_SYSTEM_PROMPT = "Answer history questions clearly and concisely."
MATH_SYSTEM_PROMPT = "Explain math step by step and include worked examples."
PHYSICS_SYSTEM_PROMPT = "Explain physics step by step and include worked examples."
TRIAGE_SYSTEM_PROMPT = (
    "Route each question to the right specialist. "
    "Use Math tutor for math/stats/ML math, History tutor for history, Physics tutor for physics."
)

history_tutor = Agent(
    name="History tutor",
    handoff_description="Specialist for history questions.",
    instructions=HISTORY_SYSTEM_PROMPT,
)

math_tutor = Agent(
    name="Math tutor",
    handoff_description="Specialist for math questions.",
    instructions=MATH_SYSTEM_PROMPT,
)

physics_tutor = Agent(
    name="Physics tutor",
    handoff_description="Specialist for physics questions.",
    instructions=PHYSICS_SYSTEM_PROMPT,
)

triage_agent = Agent(
    name="main_agent",
    model="gpt-4.1-mini",
    instructions=TRIAGE_SYSTEM_PROMPT,
    handoffs=[math_tutor, history_tutor, physics_tutor],
)


async def main() -> None:
    # result = await Runner.run(main_agent, "What is linear regression?")
    result = Runner.run_streamed(triage_agent, "What is linear regression?")

    async for event in result.stream_events():
        if event.type == "run_item_stream_event":
            print(event.name)
            print(event.item.type)

    print(result.last_agent.name)
    print(result.final_output)


if __name__ == "__main__":
    asyncio.run(main())
