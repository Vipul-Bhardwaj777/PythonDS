import asyncio


async def brew():
    print("Brewing chai")
    await asyncio.sleep(3)
    print("Brewing complete")


asyncio.run(brew())
