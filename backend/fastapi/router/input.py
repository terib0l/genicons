from fastapi import APIRouter, Request, BackgroundTasks, UploadFile, Depends
from sqlalchemy.orm import Session
from pydantic import UUID4

from module.schema import GenerateStatus, jobs
from module.dependency import ValidateUploadFile, FileTypeName
from db.session import get_db
from schemas.user import User
from crud.user import create

router = APIRouter()

validate_upload_file = ValidateUploadFile(
        max_size=12000,
        file_type=[
            FileTypeName.jpg,
            FileTypeName.png
        ],
)

@router.post("/img/save")
async def save_img(
        img: UploadFile = Depends(validate_upload_file),
        session: Session = Depends(get_db)
    ):
    """Return path of recieved img

    * args
    file: img

    * return
    handle: dict (UUID contained)
    """

    handle = GenerateStatus()

    create(session, User(id=handle.uid, img=img, img_name=img.filename))

    return handle

@router.post("/icon/generate")
async def generate_icon_from_img(
        background: BackgroundTasks,
        img: UploadFile = Depends(validate_upload_file),
        session: Session = Depends(get_db)
    ) -> GenerateStatus:
    """Start Generating icons
    
    * args
    file: img

    * return
    handle: dict (UUID contained)
    """

    handle = GenerateStatus()
    jobs[handle.uid] = handle

    create(session, User(id=handle.uid, img=img, img_name=img.filename))

    #background.add_task(start_task, handle.uid)

    return handle

@router.get("/icon/generate/status/{uid}")
async def status_of_generating(
        request: Request,
        uid: UUID4
    ) -> GenerateStatus:
    """Return Handle for progress of generating icons

    * args
    uid: UUID

    * return
    handle: dict (UUID contained)
    """
    if jobs[uid].status == "complete":
        url = request.url_for("download_products") + f"?uid={uid}"
        jobs[uid].result = url

    return jobs[uid]
