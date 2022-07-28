from sqlalchemy.ext.asyncio import AsyncSession

from app.api.crud.user import get_user


def authenticate_user(session: AsyncSession, username: str, password: str):
    user = get_user(session, username)
    if not user:
        return False
