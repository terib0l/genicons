from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm

from app.db.session import get_db
from app.api.module.auth import authenticate_user

router = APIRouter()


@router.post("/token")
async def login_for_access_token(
    form_data: OAuth2PasswordRequestForm = Depends(),
    session: AsyncSession = Depends(get_db),
):
    user = authenticate_user(session, form_data.username, form_data.password)
    return user
