from uuid import UUID
from typing import List

from fastapi import APIRouter, Depends, Query
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session
from typing import Optional

from crud.crud_product import read_rounded_square_pic, read_circle_pic, random_read, count
from db.session import get_db

router = APIRouter()

@router.get("/gallery")
def gallery(
        num: Optional[int] = Query(10, ge=10.0, le=20.0),
        session: Session = Depends(get_db)
    ):
    imgs = List()
    availble_num = count(session)

    if availble_num < num:
        imgs.extend(random_read(session, availble_num))
    else:
        imgs.extend(random_read(session, num))

    return imgs

@router.get("/icon/download/{uid}_rs", response_class=FileResponse)
async def download_rounded_square_icon(
        uid: UUID,
        session: Session = Depends(get_db)
    ):
    """Return generated rounded squere pic like icon

    * args
    uid: UUID

    * return
    rs: jpeg (Rounded-Square pic)
    """

    rounded_square_pic = read_rounded_square_pic(session, uid)

    return FileResponse(rounded_square_pic)

@router.get("/icon/download/{uid}_c", response_class=FileResponse)
async def download_circle_icon(
        uid: UUID,
        session: Session = Depends(get_db)
    ):
    """Return generated circle pic like icon

    * args
    uid: UUID

    * return
    c: jpeg (Circle pic)
    """

    circle_pic = read_circle_pic(session, uid)

    return FileResponse(circle_pic)
