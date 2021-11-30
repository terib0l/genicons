import asyncio
from uuid import UUID
from typing import Dict
from sqlalchemy.orm import Session

from module.ml_manager import StyleTransfer
from module.schema import GenerateStatus

jobs: Dict[UUID, GenerateStatus] = {}

# Dependency
def get_db():
    session = Session()
    try:
        yield session
    except:
        session.rollback()
        raise
    finally:
        session.close()

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
