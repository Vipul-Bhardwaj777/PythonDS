"""Retrieve relevant chunks from Qdrant and generate a grounded answer.
worker - rq worker --worker-class rq.worker.SimpleWorker --url redis://localhost:6379"""

from dotenv import load_dotenv
from langchain_openai import OpenAIEmbeddings
from langchain_qdrant import QdrantVectorStore
from openai import OpenAI

load_dotenv()

openai_client = OpenAI()

embedding_model = OpenAIEmbeddings(model="text-embedding-3-large")

vector_store = QdrantVectorStore.from_existing_collection(
    url="http://localhost:6333",
    embedding=embedding_model,
    collection_name="usda_nutrition",
)

SYSTEM_PROMPT = """
You are a helpful AI assistant.
Answer the user query using ONLY the context provided below from the documents.
If the answer is not in the context, say you don't know based on the available documents.
When helpful, mention the page number from the context.

Context:
{context}
"""


def process_query(user_query: str):

    relevant_result = vector_store.similarity_search(query=user_query)

    relevant_context = "\n\n\n".join(
        [
            f"Page content: {result.page_content}\n Page number: {result.metadata['page_label']}\n File location: {result.metadata['source']}"
            for result in relevant_result
        ]
    )

    response = openai_client.responses.create(
        model="gpt-5",
        instructions=SYSTEM_PROMPT.format(context=relevant_context),
        input=user_query,
    )

    return response.output_text
