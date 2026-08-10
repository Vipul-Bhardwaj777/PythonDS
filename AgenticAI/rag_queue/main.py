"""Start the Queued RAG API."""

from dotenv import load_dotenv
import uvicorn

load_dotenv()


def main():
    uvicorn.run("rag_queue.app.server:app", host="0.0.0.0", port=8000, reload=False)


if __name__ == "__main__":
    main()
