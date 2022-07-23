import os
import re
import random
import pytest
import pytest_asyncio
from faker import Faker
from pathlib import Path
from dataclasses import dataclass
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker

from app.core.config import DATABASE_URL
from app.db.session import Base
from app.db import models

CURRENT_PATH = Path(__file__).resolve().parent

FAKE = Faker()

SQLALCHEMY_DATABASE_URL = re.sub("mysql", "mysql+aiomysql", DATABASE_URL)


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
            session.add_all(
                [
                    models.User(name=FAKE.name(), email=FAKE.email(), premium=False),
                    models.User(name=FAKE.name(), email=FAKE.email(), premium=False),
                    models.User(name=FAKE.name(), email=FAKE.email(), premium=False),
                ]
            )

    await engine.dispose()

    yield


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
