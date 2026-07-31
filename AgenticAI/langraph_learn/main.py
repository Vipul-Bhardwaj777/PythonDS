from dotenv import load_dotenv
from typing_extensions import TypedDict
from typing import Annotated
from langgraph.graph.message import add_messages
from langgraph.graph import StateGraph, START, END
from langchain.chat_models import init_chat_model
from langgraph.checkpoint.mongodb import MongoDBSaver
from pprint import pprint


load_dotenv()

llm = init_chat_model(model="gpt-4.1-mini", model_provider="openai")

config = {"configurable": {"thread_id": "vipul-thread-1"}}


# Graph state
class State(TypedDict):
    messages: Annotated[list, add_messages]


# Graph nodes


def chat_bot(state: State):
    res = llm.invoke(state.get("messages", []))
    return {"messages": res}


graph_builder = StateGraph(State)

graph_builder.add_node("chat_bot", chat_bot)

graph_builder.add_edge(START, "chat_bot")
graph_builder.add_edge("chat_bot", END)


with MongoDBSaver.from_conn_string(
    "mongodb://admin:admin@localhost:27017/?authSource=admin",
    db_name="langgraph_checkpoints",
) as checkpointer:

    graph = graph_builder.compile(checkpointer=checkpointer)

    graph_result = graph.invoke(
        {"messages": [{"role": "user", "content": "Hii, who am i?"}]},
        config=config,
    )

    pprint(graph_result)
