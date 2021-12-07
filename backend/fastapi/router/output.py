from fastapi import APIRouter, Depends, Query
from fastapi.responses import StreamingResponse
from sqlalchemy.orm import Session
from pydantic import UUID4

from crud.product import read_by_uuid, random_read
from db.session import get_db

router = APIRouter()

@router.get("/gallery")
def gallery(
        session: Session = Depends(get_db),
        num: int = Query(10, ge=10.0, le=20.0)
    ):
    gallery_items = random_read(session, num)

    return gallery_items

@router.get("/icon/download/{uid}", response_class=StreamingResponse)
async def download_products(
        uid: UUID4,
        session: Session = Depends(get_db)
    ):
    """Return generated rounded squere pic like icon

    * args
    uid: UUID

    * return
    product: zip-file (contained two icons)
    """
    product = read_by_uuid(session, uid)

    if product:
        return StreamingResponse(product)
    raise Exception("product is None")
