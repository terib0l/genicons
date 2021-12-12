import asyncio
from uuid import UUID

from module.schema import jobs

async def StyleTransfer(queue: asyncio.Queue):
    for i in range(0, 10):
        await asyncio.sleep(1)
        await queue.put(i+1)
    await queue.put(None)

# Ref[progress bar]: https://stackoverflow.com/questions/64901945/how-to-send-a-progress-of-operation-in-a-fastapi-app
async def start_task(uid: UUID) -> None:
    """Start StyleTransfer
    * args
    uid: UUID
    * return
    None
    """
    queue = asyncio.Queue()
    asyncio.create_task(StyleTransfer(queue))

    while progress := await queue.get():
        jobs[uid].progress = progress

    jobs[uid].status = "complete"
