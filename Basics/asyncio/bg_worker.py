import asyncio
import time
import threading


def bg_worker():
    while True:
        time.sleep(1)
        print("Logging System health....")


async def fetch_orders():
    await asyncio.sleep(4)
    print("Orders fetched.")


thread = threading.Thread(target=bg_worker, daemon=True)
thread.start()

asyncio.run(fetch_orders())
