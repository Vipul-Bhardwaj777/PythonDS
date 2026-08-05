"""
Agents-as-tools (manager pattern) — compare with handoff_agent.py

Handoff:  router transfers ownership → specialist answers the user
as_tool:  manager keeps ownership → calls specialists like tools → manager answers
"""

from agents import Agent, Runner
from dotenv import load_dotenv
import asyncio

load_dotenv()


MATH_SYSTEM_PROMPT = "Explain math step by step with a short example. Return only the answer."
PHYSICS_SYSTEM_PROMPT = "Explain physics step by step with a short example. Return only the answer."
MANAGER_SYSTEM_PROMPT = (
    "You are a study manager. Use your specialist tools to get answers, "
    "you may call more than one specialist if the question spans topics."
)

math_tutor = Agent(
    name="Math tutor",
    instructions=MATH_SYSTEM_PROMPT,
)

physics_tutor = Agent(
    name="Physics tutor",
    instructions=PHYSICS_SYSTEM_PROMPT,
)


manager = Agent(
    name="manager",
    model="gpt-4.1-mini",
    instructions=MANAGER_SYSTEM_PROMPT,
    tools=[
        math_tutor.as_tool(
            tool_name="ask_math_tutor",
            tool_description="Ask the math tutor about math, stats, or ML math concepts.",
        ),
        physics_tutor.as_tool(
            tool_name="ask_physics_tutor",
            tool_description="Ask the physics tutor about physics topics.",
        ),
    ],
)


async def main() -> None:

    result = await Runner.run(manager, "What is linear regression?")

    print("Answered by:", result.last_agent.name)
    print(result.final_output)

    print("\n--- multi-specialist question ---\n")

    result2 = await Runner.run(
        manager,
        "In one short reply: what is a derivative in calculus, and what is velocity in physics?",
    )
    print("Answered by:", result2.last_agent.name)
    print(result2.final_output)


if __name__ == "__main__":
    asyncio.run(main())
