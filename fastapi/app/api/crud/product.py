import logging
import zipfile

from fastapi import HTTPException, status
from pydantic import UUID4
from sqlalchemy import select
from sqlalchemy.orm import selectinload
from sqlalchemy.sql.expression import func
from sqlalchemy.ext.asyncio import AsyncSession

from app.db import models
from app.api.schema.product import Product
from app.api.module.utility import remove_file

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

        logger.info("New Product: %s", product_db.product_id)
        return True

    except Exception as e:
        logger.error(e)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )


async def read_product(
    session: AsyncSession, product_id: UUID4, product_path: str
) -> bool:
    handle_jpg = [f"./rs_{product_id}.jpg", f"./c_{product_id}.jpg"]

    try:
        async with session.begin():
            statement = select(models.Product).where(
                models.Product.product_id == product_id
            )
            user_obj = await session.execute(statement)
            product = user_obj.scalars().first()

        if not product.rounded_square_icon or product.circle_icon:
            raise HTTPException(
                status_code=status.HTTP_204_NO_CONTENT, detail="No Icons yet"
            )

        with open(handle_jpg[0], "wb") as rs_file:
            rs_file.write(product.rounded_square_icon)
        with open(handle_jpg[1], "wb") as c_file:
            c_file.write(product.circle_icon)

        with zipfile.ZipFile(product_path, "w") as zip_file:
            [zip_file.write(jpg) for jpg in handle_jpg]

        return True

    except Exception as e:
        logger.error(e)
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)

    finally:
        remove_file(paths=handle_jpg)


async def delete_product(session: AsyncSession, product_id: UUID4) -> bool:
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
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )


async def read_random_products(
    session: AsyncSession, garally_num: int, garally_path: str
) -> bool:
    handle_jpg = [f"./random{i}.jpg" for i in range(1, garally_num + 1)]

    try:
        async with session.begin():
            statement = select(models.Product).order_by(func.rand()).limit(garally_num)
            products_obj = await session.execute(statement)
            products = products_obj.scalars().all()

        for i, product in enumerate(products):
            with open(handle_jpg[i], "wb") as random_file:
                random_file.write(product.rounded_square_icon)

        with zipfile.ZipFile(garally_path, "w") as zipObj:
            for jpg in handle_jpg:
                zipObj.write(jpg)

        return True

    except Exception as e:
        logger.error(e)
        return False

    finally:
        remove_file(paths=handle_jpg)
