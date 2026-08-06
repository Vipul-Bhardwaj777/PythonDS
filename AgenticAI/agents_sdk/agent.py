"""
Weather chat agent with production-style input + output guardrails.

Input guardrail  -> checks user message BEFORE the agent/tools run
Output guardrail -> checks final reply AFTER the agent finishes, BEFORE user sees it
"""

from __future__ import annotations

import asyncio
import re
from typing import Any

import requests
from agents import (
    Agent,
    GuardrailFunctionOutput,
    InputGuardrailTripwireTriggered,
    OutputGuardrailTripwireTriggered,
    RunContextWrapper,
    Runner,
    SQLiteSession,
    TResponseInputItem,
    function_tool,
)
from agents.decorators import input_guardrail, output_guardrail
from dotenv import load_dotenv
from pydantic import BaseModel, Field

from weather_prompts import (
    INPUT_GUARDRAIL_POLICY,
    JAILBREAK_PATTERNS,
    OUTPUT_GUARDRAIL_POLICY,
    OUTPUT_REFUSAL_MESSAGE,
    REFUSAL_MESSAGE,
    SECRET_PATTERNS,
    SYSTEM_PROMPT,
)

load_dotenv()


class InputJudgeResult(BaseModel):
    is_blocked: bool = Field(
        description=(
            "True = BLOCK this request (tripwire). "
            "False = ALLOW it through to the weather agent."
        )
    )
    reason: str = Field(description="Short reason for the decision (for logs / audit).")
    category: str = Field(
        description=("One of: weather, smalltalk, off_topic, harmful, jailbreak, other")
    )


class OutputJudgeResult(BaseModel):
    is_blocked: bool = Field(
        description=(
            "True = BLOCK this reply (tripwire; do not show it to the user). "
            "False = ALLOW showing this reply to the user."
        )
    )
    reason: str = Field(
        description="Short reason for the decision (for logs / audit)."
    )
    category: str = Field(
        description=(
            "One of: weather, smalltalk, off_topic, harmful, secret_leak, other"
        )
    )


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


judge_agent = Agent(
    name="input_guardrail_judge",
    model="gpt-4o-mini",
    instructions=INPUT_GUARDRAIL_POLICY,
    output_type=InputJudgeResult,
)

output_judge_agent = Agent(
    name="output_guardrail_judge",
    model="gpt-4o-mini",
    instructions=OUTPUT_GUARDRAIL_POLICY,
    output_type=OutputJudgeResult,
)


_JAILBREAK_PATTERNS = [re.compile(p, re.I) for p in JAILBREAK_PATTERNS]
_SECRET_PATTERNS = [re.compile(p, re.I) for p in SECRET_PATTERNS]


def _extract_text(input_data: str | list[TResponseInputItem]) -> str:
    if isinstance(input_data, str):
        return input_data
    parts: list[str] = []
    for item in input_data:
        if isinstance(item, dict) and item.get("role") == "user":
            content = item.get("content", "")
            if isinstance(content, str):
                parts.append(content)
    return "\n".join(parts)


def deterministic_output_block_reason(text: str) -> OutputJudgeResult | None:
    """Return a block/ hide decision without calling the LLm"""
    normalized = text.strip()
    if not normalized:
        return OutputJudgeResult(
            is_blocked=True, reason="Empty output from the agent", category="other"
        )

    for pattern in _SECRET_PATTERNS:
        if pattern.search(normalized):
            return OutputJudgeResult(
                is_blocked=True,
                reason=f"Matched secret pattern: {pattern.pattern}",
                category="secret_leak",
            )

    return None


def deterministic_block_reason(text: str) -> InputJudgeResult | None:
    """Return a block decision without calling the LLM, or None to continue."""
    normalized = text.strip()
    if not normalized:
        return InputJudgeResult(
            is_blocked=True,
            reason="Empty user message.",
            category="other",
        )
    if len(normalized) > 4000:
        return InputJudgeResult(
            is_blocked=True,
            reason="Message exceeds length limit.",
            category="other",
        )
    for pattern in _JAILBREAK_PATTERNS:
        if pattern.search(normalized):
            return InputJudgeResult(
                is_blocked=True,
                reason=f"Matched jailbreak pattern: {pattern.pattern}",
                category="jailbreak",
            )
    return None


@input_guardrail(name="weather_input_policy", run_in_parallel=False)
async def weather_input_guardrail(
    ctx: RunContextWrapper[Any],
    agent: Agent,
    input: str | list[TResponseInputItem],
) -> GuardrailFunctionOutput:
    text = _extract_text(input)

    precheck = deterministic_block_reason(text)
    if precheck is not None:
        print(
            f"Deterministic guardrail: blocked={precheck.is_blocked} "
            f"category={precheck.category} reason={precheck.reason}"
        )
        return GuardrailFunctionOutput(
            output_info=precheck,
            tripwire_triggered=precheck.is_blocked,
        )

    result = await Runner.run(judge_agent, text, context=ctx.context)
    judgment = result.final_output

    if not isinstance(judgment, InputJudgeResult):
        raise TypeError(
            f"Expected InputJudgeResult from judge agent, got {type(judgment).__name__}"
        )

    print(
        f"LLM guardrail: blocked={judgment.is_blocked} "
        f"category={judgment.category} reason={judgment.reason}"
    )
    return GuardrailFunctionOutput(
        output_info=judgment,
        tripwire_triggered=judgment.is_blocked,
    )


@output_guardrail
async def weather_output_guardrail(
    ctx: RunContextWrapper[Any], agent: Agent, output: str
) -> GuardrailFunctionOutput:

    text = output if isinstance(output, str) else str(output)
    precheck = deterministic_output_block_reason(text)

    if precheck is not None:
        print(
            f"Deterministic guardrail: blocked={precheck.is_blocked} "
            f"category={precheck.category} reason={precheck.reason}"
        )
        return GuardrailFunctionOutput(
            output_info=precheck, tripwire_triggered=precheck.is_blocked
        )

    result = await Runner.run(output_judge_agent, text, context=ctx.context)
    judgment = result.final_output

    if not isinstance(judgment, OutputJudgeResult):
        raise TypeError(
            f"Expected OutputJudgeResult from judge agent, got {type(judgment).__name__}"
        )

    print(
        f"LLM guardrail: blocked={judgment.is_blocked} "
        f"category={judgment.category} reason={judgment.reason}"
    )

    return GuardrailFunctionOutput(
        output_info=judgment, tripwire_triggered=judgment.is_blocked
    )


agent = Agent(
    name="weather_bot",
    model="gpt-4.1-mini",
    instructions=SYSTEM_PROMPT,
    tools=[get_weather],
    input_guardrails=[weather_input_guardrail],
    output_guardrails=[weather_output_guardrail],
    # output_type=AgentReply
)


async def main() -> None:
    user_session = SQLiteSession("vipul_weather_chat")

    while True:
        print()
        user_input = input("👉 ").strip()
        if not user_input or user_input.lower() == "q":
            break

        try:
            result = await Runner.run(agent, user_input, session=user_session)
            print(result.final_output)

        except InputGuardrailTripwireTriggered as exc:
            info = exc.guardrail_result.output.output_info
            print(f"Tripwire triggered: {info}")
            print(REFUSAL_MESSAGE)

        except OutputGuardrailTripwireTriggered as exc:
            info = exc.guardrail_result.output.output_info
            print(f"Tripwire triggered: {info}")
            print(OUTPUT_REFUSAL_MESSAGE)

        print()


if __name__ == "__main__":
    asyncio.run(main())
