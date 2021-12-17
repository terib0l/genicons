import asyncio
import logging

from sqlalchemy.orm import Session
from pydantic import UUID4

from module.schema import jobs
from crud import user, product

logger = logging.getLogger("genicons")

async def StyleTransfer(
        uid: UUID4,
        queue: asyncio.Queue,
        session: Session
    ):
    logger.info(StyleTransfer.__name__)

    # Make Products
    user_data = user.read(session, uid)
    product.create(session, user_data.id, user_data.img, user_data.img)

    # For progress-test
    for i in range(0, 10):
        logger.debug(i+1)
        await asyncio.sleep(1)
        await queue.put(i+1)

    await queue.put(None)

# Ref[progress bar]: https://stackoverflow.com/questions/64901945/how-to-send-a-progress-of-operation-in-a-fastapi-app
async def ml_task(
        uid: UUID4,
        session: Session
    ) -> None:
    """
    Start StyleTransfer

    Args:
        uid: UUID

    Return:
        None
    """
    logger.info(ml_task.__name__)

    queue = asyncio.Queue()
    asyncio.create_task(StyleTransfer(uid, queue, session))

    while progress := await queue.get():
        jobs[uid].progress = progress

    jobs[uid].status = "complete"
    logger.info(f"--- {ml_task.__name__} done ---")
