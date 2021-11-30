from uuid import UUID

from fastapi import APIRouter, Depends, Query
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session
from typing import Optional

from module.utilities import get_db
from module.db_manager import read_rounded_square_pic, read_circle_pic, count

router = APIRouter()

@router.get("/gallery")
def gallery(num: Optional[int] = Query(None, ge=10.0, le=20.0), session: Session = Depends(get_db)):
    if num is None:
        num = count(session)
    pass

@router.get("/icon/download/{uid}_rs", response_class=FileResponse)
async def download_rounded_square_icon(uid: UUID):
    """Return generated rounded squere pic like icon

    * args
    uid: UUID

    * return
    rs: jpeg (Rounded-Square pic)
    """

    rounded_square_pic = read_rounded_square_pic(uid)

    return FileResponse(rounded_square_pic)

@router.get("/icon/download/{uid}_c", response_class=FileResponse)
async def download_circle_icon(uid: UUID):
    """Return generated circle pic like icon

    * args
    uid: UUID

    * return
    c: jpeg (Circle pic)
    """

    circle_pic = read_circle_pic(uid)

    return FileResponse(circle_pic)
