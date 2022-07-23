import re
from typing import AsyncGenerator
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from app.core.config import DATABASE_URL

SQLALCHEMY_DATABASE_URL = re.sub("mysql", "mysql+aiomysql", DATABASE_URL)
Base = declarative_base()

ENGINE = create_async_engine(
    SQLALCHEMY_DATABASE_URL,
    encoding="utf-8",
    echo=True,
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
