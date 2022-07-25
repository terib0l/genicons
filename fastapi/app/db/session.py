from typing import AsyncGenerator
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from app.core.config import MYSQL_HOST, MYSQL_NAME, MYSQL_USER, MYSQL_PASSWORD

SQLALCHEMY_DATABASE_URL = f"mysql+aiomysql://{MYSQL_USER}:{MYSQL_PASSWORD}@{MYSQL_HOST}/{MYSQL_NAME}?charset=utf8mb4"  # noqa: E501
Base = declarative_base()

ENGINE = create_async_engine(
    SQLALCHEMY_DATABASE_URL,
    encoding="utf-8",
    echo=False,
)
async_session = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=ENGINE,
    class_=AsyncSession,
    expire_on_commit=False
    # future=True,  # <- default
)


async def get_db() -> AsyncGenerator[AsyncSession, None]:
    async with async_session() as session:
        yield session
