import logging
import zipfile

from pydantic import UUID4
from sqlalchemy import select
from sqlalchemy.orm import selectinload
from sqlalchemy.sql.expression import func
from sqlalchemy.ext.asyncio import AsyncSession

from app.db import models
from app.api.schema.product import Product

logger = logging.getLogger("genicons")


async def create_product(
    session: AsyncSession,
    product: Product,
) -> bool:
    try:
        async with session.begin():
            statement = (
                select(models.User)
                .where(models.User.id == product.users_id)
                .options(selectinload(models.User.products))
            )
            user_obj = await session.execute(statement)
            user = user_obj.scalars().first()

            product_db = models.Product(
                product_id=product.product_id,
                origin_img=product.origin_img,
                rounded_square_icon=None,
                circle_icon=None,
            )

            user.products.append(product_db)

        return True

    except Exception as e:
        logger.error(e)
        return False


async def read_product(
    session: AsyncSession, product_id: UUID4, product_path: str
) -> bool:
    try:
        async with session.begin():
            statement = select(models.Product).where(
                models.Product.product_id == product_id
            )
            product_obj = await session.execute(statement)
            product = product_obj.scalars().first()

        with zipfile.ZipFile(product_path, "w") as zip_file:
            zip_file.writestr(
                f"rs_{product.product_id}.jpg", product.rounded_square_icon
            )
            zip_file.writestr(f"c_{product.product_id}.jpg", product.circle_icon)

        return True

    except Exception as e:
        logger.error(e)
        return False


async def delete_product_by_product_id(
    session: AsyncSession, product_id: UUID4
) -> bool:
    try:
        async with session.begin():
            statement = select(models.Product).where(
                models.Product.product_id == product_id
            )
            product_obj = await session.execute(statement)
            product = product_obj.scalars().first()

            await session.delete(product)

        return True

    except Exception as e:
        logger.error(e)
        return False


async def read_random_products(
    session: AsyncSession, garally_num: int, garally_path: str
) -> bool:
    try:
        async with session.begin():
            statement = (
                select(
                    models.Product.rounded_square_icon,
                    models.Product.circle_icon,
                )
                .order_by(func.rand())
                .limit(garally_num)
            )
            products_obj = await session.execute(statement)
            products = products_obj.scalars().all()

        with zipfile.ZipFile(garally_path, "w") as zipObj:
            [
                zipObj.writestr(f"random{i}.jpg", product)
                for i, product in enumerate(products, start=1)
            ]

        return True

    except Exception as e:
        logger.error(e)
        return False
