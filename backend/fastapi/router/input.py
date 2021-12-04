from uuid import UUID

from fastapi import APIRouter, Request, BackgroundTasks, UploadFile
from fastapi.param_functions import Depends
from sqlalchemy.orm import Session

from module.schema import GenerateStatus, jobs
from module.dependency import ValidateUploadFile, FileTypeName
from db.session import get_db
from crud.crud_user import create

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
    ?
    """

    handle = GenerateStatus()
    uuid = handle.uid

    res = create(session, uuid, img.filename, img)

    return res

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

    create(session, handle.uid, img.filename, img)

    #background.add_task(start_task, handle.uid)

    return handle

@router.get("/icon/generate/status/{uid}")
async def status_of_generating(
        request: Request,
        uid: UUID
    ) -> GenerateStatus:
    """Return Handle for progress of generating icons

    * args
    uid: UUID

    * return
    handle: dict (UUID contained)
    """
    if jobs[uid].status == "complete":
        rs_url = request.url_for("download_rounded_square_icon", uid=uid)
        c_url = request.url_for("download_circle_icon", uid=uid)
        jobs[uid].result.extend([rs_url, c_url])

    return jobs[uid]
