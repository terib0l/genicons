import uuid
import logging

from fastapi import (
    APIRouter,
    BackgroundTasks,
    UploadFile,
    Depends,
    Query,
)
from sqlalchemy.ext.asyncio import AsyncSession
from pydantic import EmailStr

from app.db.session import get_db

# from app.api.module.ml_caller import caller
from app.api.module.dependency import ValidateUploadFile, FileTypeName
from app.api.schema.product import Product
from app.api.schema.user import User
from app.api.crud.product import create_product
from app.api.crud.user import create_user

logger = logging.getLogger("genicons").getChild("generator")

router = APIRouter()

validate_upload_file = ValidateUploadFile(
    max_size=16777216,
    file_type=[
        FileTypeName.jpg,
    ],
)


@router.post("/user/generate")
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
    """
    logger.info(generate_user.__name__)

    id = await create_user(session, User(name=name, email=email))

    return {"user_id": id}


@router.post("/product/generate")
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

        product_id: UUID4
    """
    logger.info(generate_product.__name__)

    product_id = uuid.uuid4()

    with img.file as data:
        await create_product(
            session,
            Product(
                product_id=product_id,
                origin_img=data.read(),
                rounded_square_icon=None,
                circle_icon=None,
                users_id=user_id,
            ),
        )

    # background.add_task(caller, product_id, session)

    return {"product_id": product_id}
