"""
FastAPI entry for queued RAG.

Full stack order (from AgenticAI, .venv on, .env with OPENAI_API_KEY):
  1. cd rag; docker compose up -d          # Qdrant :6333
  2. python rag/index.py                   # once if learning_rag missing
  3. cd rag_queue; docker compose up -d    # Valkey :6379
  4. rq worker --worker-class rq.worker.SimpleWorker --url redis://localhost:6379
  5. python -m rag_queue.main

API docs: http://localhost:8000/docs
  POST /chat?query=...  -> job_id
  GET  /job-status?job_id=...  -> result
"""

from dotenv import load_dotenv
import uvicorn
from .server import app

load_dotenv()


def main():
    uvicorn.run(app, port=8000, host="0.0.0.0")


main()
