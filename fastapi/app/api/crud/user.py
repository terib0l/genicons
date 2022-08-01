import logging
import zipfile
from typing import List, Union
from pydantic import UUID4, EmailStr
from sqlalchemy import select
from sqlalchemy.orm import selectinload
from sqlalchemy.ext.asyncio import AsyncSession

from app.db import models
from app.api.schema.user import User

logger = logging.getLogger("genicons")


async def create_user(
    session: AsyncSession, username: str, password: str, email: EmailStr
) -> Union[int, bool]:
    try:
        async with session.begin():
            session.add(models.User(name=username, password=password, email=email))
            await session.flush()

            statement = (
                select(models.User)
                .where(
                    models.User.name == username,
                    models.User.email == email,
                )
                .options(selectinload(models.User.products))
            )
            user_obj = await session.execute(statement)
            res = user_obj.scalars().first()

        return res.id

    except Exception as e:
        logger.error(e)
        return False


async def read_user(session: AsyncSession, username: str) -> Union[User, bool]:
    try:
        async with session.begin():
            statement = select(models.User).where(models.User.name == username)
            user_obj = await session.execute(statement)
            user = user_obj.scalars().first()

        return user

    except Exception as e:
        logger.error(e)
        return False


async def read_all_users(session: AsyncSession) -> Union[list, bool]:
    try:
        async with session.begin():
            statement = select(models.User)
            user_obj = await session.execute(statement)
            user = user_obj.scalars().all()

        return user

    except Exception as e:
        logger.error(e)
        return False


async def read_product_ids(
    session: AsyncSession, user_id: int
) -> Union[List[UUID4], bool]:
    product_ids = list()
    try:
        async with session.begin():
            statement = (
                select(models.User)
                .where(models.User.id == user_id)
                .options(selectinload(models.User.products))
            )
            user_obj = await session.execute(statement)
            user = user_obj.scalars().first()

        if not user:
            raise Exception("This user hasn't products!!")

        for product in user.products:
            product_ids.append(product.product_id)

        return product_ids

    except Exception as e:
        logger.error(e)
        return False


async def read_product_origins(
    session: AsyncSession, user_id: int, origins_path: str
) -> bool:
    try:
        async with session.begin():
            statement = (
                select(models.User)
                .where(models.User.id == user_id)
                .options(selectinload(models.User.products))
            )
            user_obj = await session.execute(statement)
            user = user_obj.scalars().first()

        with zipfile.ZipFile(origins_path, "w") as zip_file:
            [
                zip_file.writestr(f"{product.product_id}.jpg", product.origin_img)
                for product in user.products
            ]

        return True

    except Exception as e:
        logger.error(e)
        return False


async def update_user_email(
    session: AsyncSession, user_id: int, new_email: EmailStr
) -> bool:
    try:
        async with session.begin():
            # from sqlalchemy import update
            # statement = update(models.User).where(models.User.id == user_id).values(email=new_email)
            # await session.execute(statement)
            statement = select(models.User).where(
                models.User.id == user_id,
            )
            user_obj = await session.execute(statement)
            user = user_obj.scalars().first()

            user.email = new_email

            await session.add(user)
            await session.flush()

        return True

    except Exception as e:
        logger.error(e)
        return False


async def delete_user_by_id(session: AsyncSession, user_id: int) -> bool:
    try:
        async with session.begin():
            # from sqlalchemy import delete
            # statement = delete(models.User).where(models.User.id == user_id)
            # await session.execute(statement)
            statement = (
                select(models.User)
                .where(models.User.id == user_id)
                .options(selectinload(models.User.products))
            )
            user_obj = await session.execute(statement)
            user = user_obj.scalars().first()

            await session.delete(user)
            await session.flush()

        return True

    except Exception as e:
        logger.error(e)
        return False
