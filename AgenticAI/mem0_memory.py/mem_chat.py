from mem0 import Memory
from openai import OpenAI
from dotenv import load_dotenv
import os
import json

load_dotenv()

openai_client = OpenAI()
OPENAI_KEY = os.getenv("OPENAI_API_KEY")

config = {
    "version": "v1.1",
    "embedder": {
        "provider": "openai",
        "config": {"api_key": OPENAI_KEY, "model": "text-embedding-3-small"},
    },
    "llm": {
        "provider": "openai",
        "config": {"api_key": OPENAI_KEY, "model": "gpt-4o-mini"},
    },
    "vector_store": {
        "provider": "qdrant",
        "config": {"host": "localhost", "port": 6333},
    },
    # Depricated - now new linked entitites is used by qdran. Study the linked entities
    # "graph_store": {
    #     "provider": "neo4j",
    #     "config": {
    #         "url": os.getenv("NEO4J_URI"),
    #         "username": os.getenv("NEO_USERNAME"),
    #         "password": os.getenv("NEO_PASSWORD"),
    #     },
    # },
}

mem_client = Memory.from_config(
    config,
)


def run_agent(user_query: str):

    mem_result = mem_client.search(
        query=user_query, filters={"user_id": "vipulbhardwaj"}
    )

    memories = [
        f"Id: {mem['id']}\nMemory: {mem['memory']}" for mem in mem_result["results"]
    ]

    SYSTEM_PROMT = f"""
    Here is the context about the user:
    {json.dumps(memories)}
    """

    ai_response = openai_client.responses.create(
        model="gpt-4o-mini",
        input=[
            {"role": "system", "content": SYSTEM_PROMT},
            {"role": "user", "content": user_query},
        ],
    )

    mem_client.add(
        user_id="vipulbhardwaj",
        messages=[
            {"role": "user", "content": user_query},
            {"role": "assistant", "content": ai_response.output_text},
        ],
    )
    print(ai_response.output_text)


if __name__ == "__main__":

    while True:
        print("\n")

        user_input = input("👉 ")

        if user_input.strip().lower() == "q" or user_input.strip() == "":
            break
        run_agent(user_input)

        print("\n")
