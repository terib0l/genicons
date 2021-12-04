import asyncio
from uuid import UUID

from module.ml_manager import StyleTransfer
from module.schema import GenerateStatus, jobs

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
