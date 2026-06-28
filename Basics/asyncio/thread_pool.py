import asyncio
from concurrent.futures import ThreadPoolExecutor
import time


def check_stock(item):
    print(f"Checking stock for {item}")
    time.sleep(3)
    return f"{item} stock: 42"


async def main():
    loop = asyncio.get_running_loop()
    with ThreadPoolExecutor() as pool:
        result = await loop.run_in_executor(pool, check_stock, "Masala chai")
        print(result)


asyncio.run(main())
