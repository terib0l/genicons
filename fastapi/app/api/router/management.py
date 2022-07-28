import logging
import smtplib
from email.mime.text import MIMEText
from email.utils import formatdate
from pydantic import UUID4, EmailStr
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import APIRouter, Depends, Query, Form, HTTPException, status

from app.db.session import get_db
from app.api.crud.product import delete_product_by_product_id
from app.api.crud.user import (
    read_user,
    read_all_users,
    update_user_email,
    delete_user_by_id,
)
from app.api.module.send import caller
from app.core.config import MANAGEMENT_EMAIL, MANAGEMENT_EMAIL_PASSWD

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
async def send_contact(
    user_id: int = Query(...),
    contents: str = Form(...),
    session: AsyncSession = Depends(get_db),
):
    user = await read_user(session=session, user_id=user_id)

    if isinstance(user, bool) and user is False:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)

    if isinstance(user, dict):
        msg = MIMEText(contents, "html")
        msg["Subject"] = "GENICONS CONTACTS from {}".format(user["name"])
        msg["From"] = user["email"]
        msg["To"] = MANAGEMENT_EMAIL
        msg["Date"] = formatdate()

        smtpobj = smtplib.SMTP("smtp.gmail.com", 587, timeout=15)
        smtpobj.starttls()
        smtpobj.login(MANAGEMENT_EMAIL, MANAGEMENT_EMAIL_PASSWD)
        smtpobj.sendmail(MANAGEMENT_EMAIL, MANAGEMENT_EMAIL, msg.as_string())
        smtpobj.quit()

    return {"user_id": user_id}
