"""FastAPI entrypoint: enqueue RAG jobs and poll job status."""

from fastapi import FastAPI, Query

from rag_queue.app.models import ChatRequest
from rag_queue.queue.connection import r_queue
from rag_queue.retrieval.pipeline import process_query

app = FastAPI(title="Queued RAG")


@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/chat")
def chat(request: ChatRequest):
    job = r_queue.enqueue(process_query, request.query)
    return {"status": "queued", "job_id": job.id}


@app.get("/job-status")
def get_job_status(job_id: str = Query(..., description="Job id")):
    job = r_queue.fetch_job(job_id=job_id)
    return {"status": job.get_status(), "result": job.return_value()}
