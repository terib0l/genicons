import logging
from pydantic import UUID4, EmailStr
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import (
    APIRouter,
    Depends,
    Query,
    Form,
)

from app.db.session import get_db
from app.api.crud.product import delete_product_by_product_id
from app.api.crud.user import read_all_users, update_user_email, delete_user_by_id
from app.api.module.genicon_caller import caller

logger = logging.getLogger("genicons").getChild("management")

router = APIRouter()


@router.get("/fetch/all/users")
async def fetch_all_users(session: AsyncSession = Depends(get_db)):
    """
    Return data in user table

    Args:

    Return:

        list: [{name, id, premium, email}, ...]
    """
    return await read_all_users(session)


@router.put("/regenerate/product")
async def regenerate_product(
    product_id: UUID4 = Query(...),
    session: AsyncSession = Depends(get_db),
):
    """
    Start Generating icons

    Args:

        product_id: query(uuid4)

    Return:

        product_id: uuid4
    """
    await caller(session, product_id)

    return {"product_id": product_id}


@router.put("/update/email")
async def update_email(
    user_id: int,
    email: EmailStr,
    session: AsyncSession = Depends(get_db),
):
    """
    Start Generating icons

    Args:

        product_id: query(uuid4)

    Return:

        product_id: uuid4
    """
    await update_user_email(session, user_id, email)

    return {"user_id": user_id, "new_email": email}


@router.delete("/delete/product")
async def delete_product(
    product_id: UUID4 = Query(...),
    session: AsyncSession = Depends(get_db),
):
    """
    Start Generating icons

    Args:

        product_id: query(uuid4)

    Return:

        product_id: uuid4
    """
    await delete_product_by_product_id(session=session, product_id=product_id)

    return {"product_id": product_id}


@router.delete("/delete/user")
async def delete_user(
    user_id: int = Query(...),
    session: AsyncSession = Depends(get_db),
):
    """
    Start Generating icons

    Args:

        product_id: query(uuid4)

    Return:

        product_id: uuid4
    """
    await delete_user_by_id(session=session, user_id=user_id)

    return {"user_id": user_id}


@router.post("/send/contact")
def send_contact(contents: str = Form(...)):
    pass
