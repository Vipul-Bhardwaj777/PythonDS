"""
RQ queue client (Valkey/Redis on localhost:6379).

Not run alone — imported by server.py.
Prereq: docker compose up -d in rag_queue/ so Valkey is listening.
"""

from redis import Redis
from rq import Queue

r_queue = Queue(connection=Redis(host="localhost", port=6379))
