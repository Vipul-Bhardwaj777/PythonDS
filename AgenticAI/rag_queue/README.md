# Queued RAG

Async RAG over a Node.js PDF: offline indexing into Qdrant, FastAPI for enqueue/poll, Valkey + RQ for background retrieval and answer generation.

## Architecture

```
  Ingestion                              Query path
  ---------                              ----------
  data/nodejs.pdf
       |
  ingestion/index.py
  (chunk + embed)
       |
       v
  Qdrant :6333  <----  retrieval/pipeline.py
  nodejs_docs              (search + OpenAI)
       ^                         ^
       |                         |
       |              Valkey/RQ :6379
       |                         |
       |              POST /chat  -> job_id
       |              GET /job-status
```

## Setup

Requires `OPENAI_API_KEY` (see `.env.example`). From `AgenticAI` with the project venv active:

```powershell
cd rag_queue
docker compose up -d
cd ..
python -m rag_queue.ingestion.index
rq worker --worker-class rq.worker.SimpleWorker --url redis://localhost:6379
uvicorn rag_queue.app.server:app --host 0.0.0.0 --port 8000
```

Windows: use `SimpleWorker` — default RQ relies on `os.fork`.

API docs: http://localhost:8000/docs

## Examples

```powershell
curl -X POST http://localhost:8000/chat -H "Content-Type: application/json" -d "{\"query\": \"What is the event loop?\"}"

curl "http://localhost:8000/job-status?job_id=YOUR_JOB_ID"
```

`/job-status` returns `status` and `result` so in-progress jobs are distinct from finished ones with an empty answer.
