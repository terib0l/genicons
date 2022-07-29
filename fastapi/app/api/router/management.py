import logging
from pydantic import UUID4, EmailStr
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import (
    APIRouter,
    Depends,
    Query,
)

from app.db.session import get_db
from app.api.crud.product import delete_product_by_product_id
from app.api.crud.user import (
    read_all_users,
    update_user_email,
    delete_user_by_id,
)
from app.api.module.send import caller

logger = logging.getLogger("genicons").getChild("management")

router = APIRouter()


@router.get("/fetch/all/users")
async def fetch_all_users(session: AsyncSession = Depends(get_db)):
    """
    Return All Users

    Args:

    Return:

        users: [{id, name, password, premium, email}, ...]
    """
    return await read_all_users(session)


@router.put("/regenerate/product")
async def regenerate_product(
    product_id: UUID4 = Query(...),
    session: AsyncSession = Depends(get_db),
):
    """
    Regenerate Icons

    Args:

        product_id: Query(uuid4)

    Return:

        product_id: uuid4
    """
    await caller(session, product_id)

    return {"product_id": product_id}


@router.put("/update/email")
async def update_email(
    user_id: int = Query(...),
    new_email: EmailStr = Query(...),
    session: AsyncSession = Depends(get_db),
):
    """
    Update User's Email

    Args:

        user_id: Query(int)
        new_email: Query(email)

    Return:

        email: email
    """
    await update_user_email(session, user_id, new_email)

    return {"email": new_email}


@router.delete("/delete/product")
async def delete_product(
    product_id: UUID4 = Query(...),
    session: AsyncSession = Depends(get_db),
):
    """
    Delete Product

    Args:

        product_id: Query(uuid4)

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
    Delete User

    Args:

        user_id: Query(int)

    Return:

        user_id: int
    """
    await delete_user_by_id(session=session, user_id=user_id)

    return {"user_id": user_id}
