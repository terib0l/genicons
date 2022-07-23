import logging

from fastapi import HTTPException, status
from typing import List
from pydantic import UUID4, EmailStr
from sqlalchemy import select
from sqlalchemy.orm import selectinload
from sqlalchemy.ext.asyncio import AsyncSession

from app.db import models
from app.api.schema.user import User

logger = logging.getLogger("genicons")


async def create_user(session: AsyncSession, user: User) -> int:
    try:
        async with session.begin():
            session.add(models.User(name=user.name, email=user.email))
            await session.flush()

            statement = (
                select(models.User)
                .where(
                    models.User.name == user.name,
                    models.User.email == user.email,
                )
                .options(selectinload(models.User.products))
            )
            user_obj = await session.execute(statement)
            res = user_obj.scalars().first()

        return res.id

    except Exception as e:
        logger.error(e)
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)


async def read_all_users(session: AsyncSession):
    try:
        async with session.begin():
            statement = select(models.User)
            user_obj = await session.execute(statement)
            user = user_obj.scalars().all()

        return user

    except Exception as e:
        logger.error(e)
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)


async def read_product_ids(
    session: AsyncSession, name: str, email: EmailStr
) -> List[UUID4]:
    product_ids = list()
    try:
        async with session.begin():
            statement = (
                select(models.User)
                .where(models.User.name == name, models.User.email == email)
                .options(selectinload(models.User.products))
            )
            user_obj = await session.execute(statement)
            user = user_obj.scalars().first()

        for product in user.products:
            product_ids.append(product.product_id)

        return product_ids

    except Exception as e:
        logger.error(e)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )


async def update_user_email(
    session: AsyncSession, name: str, new_email: EmailStr
) -> bool:
    try:
        async with session.begin():
            statement = select(models.User).where(
                models.User.name == name,
            )
            user_obj = await session.execute(statement)
            user = user_obj.scalars().first()

            user.email = new_email

            await session.add(user)
            await session.flush()

        return True

    except Exception as e:
        logger.error(e)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )


async def delete_user(session: AsyncSession, name: str, email: EmailStr) -> bool:
    try:
        async with session.begin():
            statement = (
                select(models.User)
                .where(models.User.name == name, models.User.email == email)
                .options(selectinload(models.User.products))
            )
            user_obj = await session.execute(statement)
            user = user_obj.scalars().first()

            await session.delete(user)
            await session.flush()

        return True

    except Exception as e:
        logger.error(e)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )
