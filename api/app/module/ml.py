import asyncio

from pydantic import UUID4

from module.schema import jobs

async def StyleTransfer(
        queue: asyncio.Queue
    ):
    for i in range(0, 10):
        await asyncio.sleep(1)
        await queue.put(i+1)
    await queue.put(None)

# Ref[progress bar]: https://stackoverflow.com/questions/64901945/how-to-send-a-progress-of-operation-in-a-fastapi-app
async def ml_task(
        uid: UUID4
    ) -> None:
    """
    Start StyleTransfer

    Args:
        uid: UUID

    Return:
        None
    """
    queue = asyncio.Queue()
    asyncio.create_task(StyleTransfer(queue))

    while progress := await queue.get():
        jobs[uid].progress = progress

    jobs[uid].status = "complete"
