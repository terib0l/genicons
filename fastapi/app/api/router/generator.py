import logging
import uuid

from fastapi import APIRouter, BackgroundTasks, UploadFile, Depends
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.api.module.ml_caller import caller
from app.api.module.dependency import ValidateUploadFile, FileTypeName
from app.api.schema.user import User
from app.api.crud.user import create

logger = logging.getLogger("genicons").getChild("generator")

router = APIRouter()

validate_upload_file = ValidateUploadFile(
    max_size=16777216,
    file_type=[
        FileTypeName.jpg,
    ],
)


@router.post("/product/generate")
def generate_product(
    background: BackgroundTasks,
    img: UploadFile = Depends(validate_upload_file),
    session: Session = Depends(get_db),
):
    """
    Start Generating icons

    Args:

        img: File

    Return:

        uid: UUID4
    """
    logger.info(generate_product.__name__)

    uid = uuid.uuid4()

    with img.file as data:
        create(session, User(id=uid, img=data.read(), img_name=img.filename))

    background.add_task(caller, uid, session)

    return {"uid": uid}
