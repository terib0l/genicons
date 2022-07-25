import os
import random
import uuid
import asyncio
import pytest
import pytest_asyncio
from typing import Generator
from faker import Faker
from pathlib import Path
from dataclasses import dataclass
from sqlalchemy import select
from sqlalchemy.orm import sessionmaker, selectinload
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from httpx import AsyncClient

from main import app
from app.db import models
from app.db.session import Base
from app.core.config import MYSQL_HOST, MYSQL_NAME, MYSQL_USER, MYSQL_PASSWORD

CURRENT_PATH = Path(__file__).resolve().parent

FAKE = Faker()

SQLALCHEMY_DATABASE_URL = f"mysql+aiomysql://{MYSQL_USER}:{MYSQL_PASSWORD}@{MYSQL_HOST}/{MYSQL_NAME}?charset=utf8mb4"  # noqa: E501

PRODUCT_IDS = [
    uuid.uuid4(),
    uuid.uuid4(),
    uuid.uuid4(),
]


@pytest.fixture(scope="session")
def event_loop() -> Generator:
    """
    Create an instance of the default event loop for each test case.
    """
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest_asyncio.fixture(scope="function")
async def async_client():
    async with AsyncClient(app=app, base_url="http://127.0.0.1:8888/") as client:
        yield client


@pytest_asyncio.fixture(scope="function", autouse=True)
async def async_session():
    engine = create_async_engine(SQLALCHEMY_DATABASE_URL, echo=False)

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)

    async_session = sessionmaker(
        bind=engine, class_=AsyncSession, expire_on_commit=False
    )
    async with async_session() as session:
        async with session.begin():
            # Registration init-users
            session.add_all(
                [
                    models.User(name=FAKE.name(), email=FAKE.email(), premium=False),
                    models.User(name=FAKE.name(), email=FAKE.email(), premium=False),
                    models.User(name=FAKE.name(), email=FAKE.email(), premium=False),
                ]
            )

            # Registration init-products
            names = os.listdir(str(Path(CURRENT_PATH, "img/")))
            for i, name in enumerate(names, start=1):
                path = str(Path(CURRENT_PATH, "img/", name))

                statement = (
                    select(models.User)
                    .where(models.User.id == i)
                    .options(selectinload(models.User.products))
                )
                user_obj = await session.execute(statement)
                user = user_obj.scalars().first()

                user.products.append(
                    models.Product(
                        product_id=PRODUCT_IDS[i - 1],
                        origin_img=open(path, "rb").read(),
                        circle_icon=open(path, "rb").read(),
                        rounded_square_icon=open(path, "rb").read(),
                    )
                )

    await engine.dispose()


@dataclass
class Image:
    name: str
    path: str


@pytest.fixture(scope="function")
def random_image():
    name = random.choice(os.listdir(str(Path(CURRENT_PATH, "img/"))))
    path = str(Path(CURRENT_PATH, "img/", name))

    image = Image(name=name, path=path)

    return image


@pytest.fixture(scope="function")
def random_user():
    return {
        "name": FAKE.name(),
        "email": FAKE.email(),
    }


@pytest.fixture(scope="function")
def product_id():
    return random.choice(PRODUCT_IDS)
