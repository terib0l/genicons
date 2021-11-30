import asyncio

async def StyleTransfer(queue: asyncio.Queue):
    for i in range(0, 10):
        await asyncio.sleep(1)
        await queue.put(i+1)
    await queue.put(None)
