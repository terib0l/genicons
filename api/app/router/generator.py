import logging

from fastapi import APIRouter, Request, BackgroundTasks, UploadFile, Depends
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from pydantic import UUID4

from module.ml import ml_task
from module.schema import GenerateStatus, jobs
from module.dependency import ValidateUploadFile, FileTypeName
from db.session import get_db
from schemas.user import User
from crud import user

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

@router.get("/read")
def read_all(
        session: Session = Depends(get_db)
    ):
    """
    Return data in user table

    Args:
    Return:

        id: UUID
        img: File
        img_name: Str
    """
    try:
        logger.info(read_all.__name__)

        return user.all_read(session)

    except Exception as e:
        logger.error(e)
        return JSONResponse(status_code=500, content="Internal Server Error")

@router.post("/img/save")
async def save_img(
        img: UploadFile = Depends(validate_upload_file),
        session: Session = Depends(get_db)
    ):
    """
    Return path of recieved img

    Args:

        img: File

    Return:

        handle: Dict (UUID contained)
    """
    try:
        logger.info(save_img.__name__)

        handle = GenerateStatus()

        with img.file as data:
            user.create(
                    session,
                    User(
                        id=handle.uid,
                        img=data.read(),
                        img_name=img.filename
                    )
            )

        return handle

    except Exception as e:
        logger.error(e)
        return JSONResponse(status_code=500, content="Internal Server Error")

@router.post("/product/generate")
async def generate_product(
        background: BackgroundTasks,
        img: UploadFile = Depends(validate_upload_file),
        session: Session = Depends(get_db)
    ):
    """
    Start Generating icons
    
    Args:

        img: File

    Return:

        handle: Dict (UUID contained)
    """
    try:
        handle = GenerateStatus()
        jobs[handle.uid] = handle

        with img.file as data:
            user.create(
                    session,
                    User(
                        id=handle.uid,
                        img=data.read(),
                        img_name=img.filename
                    )
            )

        background.add_task(ml_task, handle.uid)

        return handle

    except Exception as e:
        logger.error(e)
        return JSONResponse(status_code=500, content="Internal Server Error")

@router.get("/product/generate/status/{uid}")
async def generating_status(
        request: Request,
        uid: UUID4
    ):
    """
    Return Handle for progress of generating icons

    Args:

        uid: UUID

    Return:

        handle: Dict (UUID contained)
    """
    try:
        logger.info(uid)
        logger.info(type(uid))
        if jobs[uid].status == "complete":
            url = request.url_for("download_products", uid=uid)
            logger.info(url)
            jobs[uid].url = url

        return jobs[uid]

    except Exception as e:
        logger.error(e)
        return JSONResponse(status_code=500, content="Internal Server Error")
