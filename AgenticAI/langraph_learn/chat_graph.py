from dotenv import load_dotenv
from typing_extensions import TypedDict
from typing import Optional, Literal
from langgraph.graph import StateGraph, START, END
from openai import OpenAI


load_dotenv()

openai_client = OpenAI()

SYSTEM_PROMPT = """
You judge if the assistant answer is good enough for the user question.
Reply with only: good  OR  bad
"""


class State(TypedDict):
    user_query: str
    llm_output: Optional[str]
    is_good: Optional[bool]


def chat_bot(state: State):
    chat_res = openai_client.chat.completions.create(
        model="gpt-4.1-mini",
        messages=[{"role": "user", "content": state.get("user_query")}],
    )

    return {"llm_output": chat_res.choices[0].message.content}


def chat_bot_large(state: State):
    chat_res = openai_client.chat.completions.create(
        model="gpt-4.1", messages=[{"role": "user", "content": state.get("user_query")}]
    )

    return {"llm_output": chat_res.choices[0].message.content}


def evalutate(state: State):
    chat_res = openai_client.chat.completions.create(
        model="gpt-4.1",
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {
                "role": "user",
                "content": (
                    f"Question: {state.get('user_query')}\n"
                    f"Answer: {state.get('llm_output')}"
                ),
            },
        ],
    )

    verdict = (chat_res.choices[0].message.content).strip().lower()

    return {"is_good": verdict == "good"}


def evaluation_route(state: State) -> Literal["chat_bot_large", "end_node"]:

    if state.get("is_good"):
        return "end_node"

    return "chat_bot_large"


def end_node(state: State):
    return state


graph_builder = StateGraph(State)

graph_builder.add_node("chat_bot", chat_bot)
graph_builder.add_node("chat_bot_large", chat_bot_large)
graph_builder.add_node("evalutate", evalutate)
graph_builder.add_node("end_node", end_node)

graph_builder.add_edge(START, "chat_bot")
graph_builder.add_edge("chat_bot", "evalutate")
graph_builder.add_conditional_edges("evalutate", evaluation_route)
graph_builder.add_edge("chat_bot_large", "end_node")
graph_builder.add_edge("end_node", END)

graph = graph_builder.compile()
graph_result = graph.invoke({"user_query": "What is 2 + 2"})

print(graph_result)
