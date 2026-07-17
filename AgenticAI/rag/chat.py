"""
Interactive RAG chat CLI (no queue).

Prereqs: Qdrant :6333, collection learning_rag indexed (see rag/index.py), OPENAI_API_KEY.
"""

from openai import OpenAI
from dotenv import load_dotenv
from langchain_openai import OpenAIEmbeddings
from langchain_qdrant import QdrantVectorStore


load_dotenv()

openai_client = OpenAI()

embedding_model = OpenAIEmbeddings(model="text-embedding-3-large")

vector_store = QdrantVectorStore.from_existing_collection(
    embedding=embedding_model,
    url="http://localhost:6333",
    collection_name="learning_rag",
)


SYSTEM_PROMPT = """
You are a helpful AI assistant named Billy.
Answer the user query using ONLY the context provided below from the documents.
If the answer is not in the context, say you don't know based on the available documents.
When helpful, mention the page number from the context.

Context:
{context}
"""


def run_agent(user_input):

    relevant_result = vector_store.similarity_search(query=user_input)

    relevant_context = "\n\n\n".join(
        [
            f"Page content: {result.page_content}\n Page number: {result.metadata['page_label']}\n File Location: {result.metadata['source']}"
            for result in relevant_result
        ]
    )

    result = openai_client.chat.completions.create(
        model="gpt-5",
        messages=[
            {
                "role": "system",
                "content": SYSTEM_PROMPT.format(context=relevant_context),
            },
            {"role": "user", "content": user_input},
        ],
    )

    print(result.choices[0].message.content)


if __name__ == "__main__":

    while True:
        print("\n")

        user_query = input("Ask anything 👉 ")

        if user_query == "q" or user_query == "":
            break

        run_agent(user_query)

        print("\n")
