"""
FastAPI app: enqueue RAG jobs and poll results.

Do not run this file directly. Start via:
  python -m rag_queue.main

Or: uvicorn rag_queue.server:app --host 0.0.0.0 --port 8000

Endpoints:
  GET  /              health
  POST /chat?query=   enqueue job -> {job_id}
  GET  /job-status?job_id=  fetch result

Requires Valkey + RQ worker running (see queue/worker.py header).
"""

from fastapi import FastAPI, Query
from .queue.worker import process_query
from .client.rq_client import r_queue

app = FastAPI()


@app.get("/")
def root_read():
    return {"status": "Server is up and running"}


@app.post("/chat")
def chat(query: str = Query(..., description="The chat query of user.")):

    job = r_queue.enqueue(process_query, query)

    return {"status": "queued", "job_id": job.id}


@app.get("/job-status")
def get_job_status(job_id: str = Query(..., description="Job id")):
    job = r_queue.fetch_job(job_id=job_id)
    result = job.return_value()

    return {"result": result}
