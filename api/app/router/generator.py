import logging
import uuid

from fastapi import APIRouter, BackgroundTasks, UploadFile, Depends
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session

from module.ml_caller import caller
from module.dependency import ValidateUploadFile, FileTypeName
from db.session import get_db
from schemas.user import User
from crud.user import create

logger = logging.getLogger("genicons")

router = APIRouter(
        tags=["generator"]
)

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
        session: Session = Depends(get_db)
    ):
    """
    Start Generating icons
    
    Args:

        img: File

    Return:

        uid: UUID4
    """
    logger.info(generate_product.__name__)

    try:
        uid = uuid.uuid4()

        with img.file as data:
            create(
                    session,
                    User(
                        id=uid,
                        img=data.read(),
                        img_name=img.filename
                    )
            )

        background.add_task(caller, uid, session)

        return {"uid": uid}

    except Exception as e:
        logger.error(e)
        return JSONResponse(status_code=500, content="Internal Server Error")
