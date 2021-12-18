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
    logger.info(generate_product.__name__)

    try:
        handle = GenerateStatus()
        jobs[handle.uid] = handle

        with img.file as data:
            create(
                    session,
                    User(
                        id=handle.uid,
                        img=data.read(),
                        img_name=img.filename
                    )
            )

        background.add_task(ml_task, handle.uid, session)

        return handle.uid

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
    logger.info(generating_status.__name__)

    try:
        if jobs[uid].status == "complete":
            url = request.url_for("download_products", uid=uid)
            return JSONResponse(status_code=200, content={"url": url})

        return JSONResponse(status_code=204, content={"status": jobs[uid].status, "progress": jobs[uid].progress})

    except Exception as e:
        logger.error(e)
        return JSONResponse(status_code=500, content="Internal Server Error")
