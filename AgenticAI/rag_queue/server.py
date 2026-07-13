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
