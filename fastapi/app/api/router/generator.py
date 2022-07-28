import logging
from uuid import uuid4
from pydantic import EmailStr
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import (
    APIRouter,
    BackgroundTasks,
    UploadFile,
    Depends,
    Query,
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
    name: str = Query(...),
    email: EmailStr = Query(...),
    session: AsyncSession = Depends(get_db),
):
    """
    Generate user

    Args:

        name: query(str)
        email: query(EmailStr)

    Return:

        user_id: int
    """
    id = await create_user(session, User(name=name, email=email))

    if not id:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)

    logger.info("generate_user() created new user_id: %s", id)
    return {"user_id": id}


@router.post("/generate/product")
async def generate_product(
    background: BackgroundTasks,
    user_id: int = Query(...),
    img: UploadFile = Depends(validate_upload_file),
    session: AsyncSession = Depends(get_db),
):
    """
    Start Generating icons

    Args:

        user_id: query(int)
        img: post-data(File)

    Return:

        product_id: uuid4
    """
    logger.info("generate_product be acessed!!")
    product_id = uuid4()

    with img.file as data:
        res = await create_product(
            session,
            Product(
                product_id=product_id,
                origin_img=data.read(),
                rounded_square_icon=None,
                circle_icon=None,
                users_id=user_id,
            ),
        )

        if not res:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)

    background.add_task(caller, session, product_id)

    logger.info("generate_product() created new product: %s", product_id)
    return {"product_id": product_id}
