import logging

from sqlalchemy.orm import Session
from pydantic import UUID4

from app.api.crud import user, product

logger = logging.getLogger("genicons").getChild("ml_caller")


async def caller(uid: UUID4, session: Session):
    logger.info(caller.__name__)

    # Request to model of StyleTransfer for make Products
    user_data = user.read(session, uid)
    """
    response = requests.get(f'http://{uid}')
    data = response.json()
    product.create(session, uid, data["rs"], data["c"])
    """
    product.create(session, user_data.id, user_data.img, user_data.img)

    logger.info("ml done")
