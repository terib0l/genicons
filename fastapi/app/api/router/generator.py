import logging
import smtplib
from uuid import uuid4
from pydantic import EmailStr
from email.mime.text import MIMEText
from email.utils import formatdate
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import (
    APIRouter,
    BackgroundTasks,
    UploadFile,
    Depends,
    Form,
    HTTPException,
    status,
)

from app.db.session import get_db
from app.api.schema.product import Product
from app.api.schema.user import User
from app.api.crud.product import create_product
from app.api.crud.user import create_user
from app.api.module.dependency import ValidateUploadFile, FileTypeName
from app.api.module.send import caller
from app.api.module.auth import get_password_hash, get_current_user
from app.core.config import MANAGEMENT_EMAIL, MANAGEMENT_EMAIL_PASSWD

logger = logging.getLogger("genicons").getChild("generator")

router = APIRouter()

validate_upload_file = ValidateUploadFile(
    max_size=16777216,
    file_type=[
        FileTypeName.jpg,
    ],
)


@router.post("/generate/user")
async def generate_user(
    username: str = Form(...),
    email: EmailStr = Form(...),
    password: str = Form(...),
    session: AsyncSession = Depends(get_db),
):
    """
    Generate user

    Args:

        username: Form(str)
        password: Form(str)
        email: Form(email)

    Return:

        user_id: int
    """
    name = "".join(username.lower().split())

    id = await create_user(
        session, username=name, password=get_password_hash(password), email=email
    )

    if not id:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)

    logger.info("generate_user() created new user_id: %s", id)
    return {"user_id": id}


@router.post("/generate/product")
async def generate_product(
    background: BackgroundTasks,
    user: User = Depends(get_current_user),
    image: UploadFile = Depends(validate_upload_file),
    session: AsyncSession = Depends(get_db),
):
    """
    Start Generating icons

    Args:

        token: Bearer(jwt)
        image: Form(jpeg)

    Return:

        product_id: uuid4
    """
    product_id = uuid4()

    with image.file as img:
        image_bytes = img.read()
        res = await create_product(
            session,
            Product(
                product_id=product_id,
                origin_img=image_bytes,
                rounded_square_icon=None,
                circle_icon=None,
                users_id=user.id,
            ),
        )

        if not res:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)

        background.add_task(caller, image_bytes, product_id)

    logger.debug("generate_product() created new product: %s", product_id)

    return {"product_id": product_id}


@router.post("/send/contact")
async def send_contact(
    user: User = Depends(get_current_user),
    contents: str = Form(...),
):
    """
    Send Contact Email

    Args:

        token: Bearer(jwt)
        contents: Form(str)

    Return:

        username: str
        email: email
    """
    msg = MIMEText(f"From {user.name}: {user.email}\r\n\r\n{contents}")
    msg["Subject"] = "GENICONS CONTACTS"
    msg["From"] = user.email
    msg["To"] = MANAGEMENT_EMAIL
    msg["Date"] = formatdate()

    smtpobj = smtplib.SMTP("smtp.gmail.com", 587, timeout=15)
    smtpobj.starttls()
    smtpobj.login(MANAGEMENT_EMAIL, MANAGEMENT_EMAIL_PASSWD)
    smtpobj.sendmail(MANAGEMENT_EMAIL, MANAGEMENT_EMAIL, msg.as_string())
    smtpobj.quit()

    return {"username": user.name, "email": user.email}

