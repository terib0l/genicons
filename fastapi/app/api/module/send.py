import logging

from pydantic import UUID4
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.db import models

logger = logging.getLogger("genicons").getChild("send")


async def caller(
    session: AsyncSession,
    product_id: UUID4,
):
    logger.debug("genicon_caller(): start")

    try:
        # Request to model of StyleTransfer for make Products
        async with session.begin():
            statement = select(models.Product).where(
                models.Product.product_id == product_id
            )
            product_obj = await session.execute(statement)
            product = product_obj.scalars().first()

            product.rounded_square_icon = product.origin_img
            product.circle_icon = product.origin_img
            session.add(product)
            await session.flush()
        """
        response = requests.get(f'http://{uid}')
        data = response.json()
        product.create(session, uid, data["rs"], data["c"])
        """

        logger.debug("genicon_caller(): done")
    except Exception as e:
        logger.error("genicon_caller(): error => %s", e)
