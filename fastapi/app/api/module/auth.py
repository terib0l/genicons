import logging
from typing import Union
from jose import jwt, JWTError, ExpiredSignatureError
from datetime import datetime, timedelta, timezone
from passlib.context import CryptContext
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer

from app.api.crud.user import read_user
from app.db.session import get_db
from app.core.config import SECRET_KEY, ALGORITHM

logger = logging.getLogger("genicons").getChild("auth")

oauth2_schema = OAuth2PasswordBearer(tokenUrl="token")

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

credentials_exception = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Could not validate credentials",
    headers={"WWW-Authenticate": "Bearer"},
)


def get_password_hash(password):
    return pwd_context.hash(password)


def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


async def authenticate_user(session: AsyncSession, username: str, password: str):
    user = await read_user(session, username)
    if not user:
        logger.error("read_user_by_name() returns None")
        return False
    if not verify_password(password, user.password):
        logger.error("verify_password() returns None")
        return False
    return user


def create_access_token(data: dict, expires_data: Union[timedelta, None] = None):
    to_encode = data.copy()
    if expires_data:
        expire = datetime.now(timezone.utc) + expires_data
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, str(SECRET_KEY), algorithm=ALGORITHM)
    return encoded_jwt


async def get_current_user(
    session: AsyncSession = Depends(get_db), token: str = Depends(oauth2_schema)
):
    try:
        payload = jwt.decode(token, str(SECRET_KEY), algorithms=[ALGORITHM])
        username = payload.get("sub")
        if username is None:
            raise credentials_exception
    except ExpiredSignatureError:
        logger.error("This token is expired")
        raise credentials_exception
    except JWTError:
        logger.error("This token is invalid in any way")
        raise credentials_exception
    user = await read_user(session, username)
    if user is None:
        raise credentials_exception
    return user
