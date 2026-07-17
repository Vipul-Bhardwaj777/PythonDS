r"""
RQ job: RAG retrieval + OpenAI answer.

Prereqs: Qdrant :6333, Valkey :6379, indexed collection learning_rag, OPENAI_API_KEY.

Run worker (Windows — use SimpleWorker; default RQ uses os.fork and crashes):
  cd AgenticAI
  .\.venv\Scripts\Activate.ps1
  rq worker --worker-class rq.worker.SimpleWorker --url redis://localhost:6379

Then start API: python -m rag_queue.main
Use /docs: POST /chat -> GET /job-status with the new job_id.
"""

from openai import OpenAI
from dotenv import load_dotenv
from langchain_qdrant import QdrantVectorStore
from langchain_openai import OpenAIEmbeddings

load_dotenv()

openai_client = OpenAI()

embedding_model = OpenAIEmbeddings(model="text-embedding-3-large")

vector_store = QdrantVectorStore.from_existing_collection(
    url="http://localhost:6333",
    embedding=embedding_model,
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


def process_query(user_query: str):

    relevant_result = vector_store.similarity_search(query=user_query)

    relevant_context = "\n\n\n".join(
        [
            f"Page content: {result.page_content}\n Page number: {result.metadata['page_label']}\n File location: {result.metadata['source']}"
            for result in relevant_result
        ]
    )

    chat_result = openai_client.chat.completions.create(
        model="gpt-5",
        messages=[
            {
                "role": "system",
                "content": SYSTEM_PROMPT.format(context=relevant_context),
            },
            {"role": "user", "content": user_query},
        ],
    )

    print(chat_result.choices[0].message.content)
    return chat_result.choices[0].message.content
