from dotenv import load_dotenv
from typing_extensions import TypedDict
from typing import Annotated
from langgraph.graph.message import add_messages
from langgraph.graph import StateGraph, START, END
from langchain.chat_models import init_chat_model

load_dotenv()

llm = init_chat_model(model="gpt-4.1-mini", model_provider="openai")


# Graph state
class State(TypedDict):
    messages: Annotated[list, add_messages]


# Graph nodes


def chat_bot(state: State):
    res = llm.invoke(state.get("messages", []))
    return {"messages": res}


def sample_node(state: State):
    return {"messages": ["Hii from the sample_node"]}


graph_builder = StateGraph(State)

graph_builder.add_node("chat_bot", chat_bot)
graph_builder.add_node("sample_node", sample_node)

graph_builder.add_edge(START, "chat_bot")
graph_builder.add_edge("chat_bot", "sample_node")
graph_builder.add_edge("sample_node", END)

graph = graph_builder.compile()

graph_result = graph.invoke({"messages": ["Hii, my name is Vipul"]})

print(graph_result)
