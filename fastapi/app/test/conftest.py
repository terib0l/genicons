import random
import asyncio
import pytest
import pytest_asyncio
from httpx import AsyncClient
from faker import Faker
from typing import Generator
from pathlib import Path
from passlib.context import CryptContext
from dataclasses import dataclass
from sqlalchemy import select
from sqlalchemy.orm import sessionmaker, selectinload
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession

from main import app
from app.db import models
from app.db.session import Base
from app.core.config import MYSQL_HOST, MYSQL_NAME, MYSQL_USER, MYSQL_PASSWORD

CURRENT_PATH = Path(__file__).resolve().parent

FAKE = Faker()

USERS = [
    [FAKE.user_name(), FAKE.password(length=20), FAKE.email()],
    [FAKE.user_name(), FAKE.password(length=20), FAKE.email()],
    [FAKE.user_name(), FAKE.password(length=20), FAKE.email()],
]
PRODUCT_IDS = [FAKE.uuid4() for _ in range(3)]
PRODUCT_ORIGINS = [FAKE.image(image_format="jpeg") for _ in range(3)]

SQLALCHEMY_DATABASE_URL = f"mysql+aiomysql://{MYSQL_USER}:{MYSQL_PASSWORD}@{MYSQL_HOST}/{MYSQL_NAME}?charset=utf8mb4"  # noqa: E501

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


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


@pytest_asyncio.fixture(scope="function")
async def token_header(async_client):
    user_id = random.choice(range(3))
    response = await async_client.post(
        url="token",
        data={
            "username": USERS[user_id][0],
            "password": USERS[user_id][1],
        },
    )

    data = response.json()
    access_token = data["access_token"]

    return {"Authorization": f"Bearer {access_token}"}


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
                    models.User(
                        name=USERS[i][0],
                        password=pwd_context.hash(USERS[i][1]),
                        email=USERS[i][2],
                        premium=False,
                    )
                    for i in range(3)
                ]
            )

            # Registration init-products
            for i in range(3):
                statement = (
                    select(models.User)
                    .where(models.User.id == (i + 1))
                    .options(selectinload(models.User.products))
                )
                user_obj = await session.execute(statement)
                user = user_obj.scalars().first()

                user.products.append(
                    models.Product(
                        product_id=PRODUCT_IDS[i],
                        origin_img=PRODUCT_ORIGINS[i],
                        circle_icon=PRODUCT_ORIGINS[i],
                        rounded_square_icon=PRODUCT_ORIGINS[i],
                    )
                )

    await engine.dispose()


@dataclass
class Image:
    name: str
    img: bytes


@pytest.fixture(scope="function")
def random_image():
    return Image(name=FAKE.color_name(), img=FAKE.image(image_format="jpeg"))


@pytest.fixture(scope="function")
def random_user():
    return {
        "name": FAKE.user_name(),
        "password": FAKE.password(length=20),
        "email": FAKE.email(),
    }


@pytest.fixture(scope="function")
def random_contents():
    psuedo_sentence = FAKE.sentence()
    return f"PYTEST: {psuedo_sentence}"


@pytest.fixture(scope="function")
def product_id():
    return random.choice(PRODUCT_IDS)
