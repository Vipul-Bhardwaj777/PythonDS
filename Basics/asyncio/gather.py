import asyncio

async def brew(name, timer):
    print(f'Started brewing {name}')
    await asyncio.sleep(timer)
    print(f'Brewing ended for {name}')

async def main():
    await asyncio.gather(
        brew('Masala chai',3),
        brew('Ginger chai',2),
        brew('Lemon chai',1)
    )

asyncio.run(main())