"""Redis/Valkey connection and default RQ queue."""

from redis import Redis
from rq import Queue

r_queue = Queue(connection=Redis(host="localhost", port=6379))
