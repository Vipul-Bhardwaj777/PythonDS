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

# higher = stricter
MIN_RELEVANCE_SCORE = 0.55

REFUSAL_MESSAGE = (
    "I don't know based on the available documents. "
    "No sufficiently relevant passages were found to answer confidently. "
    "This is not medical advice."
)

SYSTEM_PROMPT = """
You answer questions using ONLY the document context below.
If the context does not contain the answer, say you do not know.
Cite page numbers when they are available.
Do not invent facts, numbers, or recommendations that are not in the context.
This is not medical advice. Do not diagnose or prescribe treatment.

Context:
{context}
"""


def process_query(user_query: str):
    relevant_result = vector_store.similarity_search(
        query=user_query,
        score_threshold=MIN_RELEVANCE_SCORE,
    )

    if not relevant_result:
        return REFUSAL_MESSAGE

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
