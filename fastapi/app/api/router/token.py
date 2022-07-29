import logging
from datetime import timedelta
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm

from app.db.session import get_db
from app.api.module.auth import (
    authenticate_user,
    create_access_token,
)
from app.core.config import ACCESS_TOKEN_EXPIRE_MINUTES

logger = logging.getLogger("genicons").getChild("token")

router = APIRouter()


@router.post("/token")
async def login_for_access_token(
    form_data: OAuth2PasswordRequestForm = Depends(),
    session: AsyncSession = Depends(get_db),
):
    """
    Get Token

    Args:

        name: Form(str)
        password: Form(str)

    Return:

        access_token: jwt
        token_type: str
    """
    user = await authenticate_user(session, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.name}, expires_data=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}
