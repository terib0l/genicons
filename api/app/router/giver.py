from fastapi import APIRouter, Depends, Query
from fastapi.responses import StreamingResponse
from sqlalchemy.orm import Session
from pydantic import UUID4

from crud.product import read_by_uuid, random_read
from db.session import get_db

router = APIRouter(
        tags=["giver"]
        )

@router.get("/gallery/{num}/download")
def gallery(
        num: int = Query(3, ge=1.0, le=12.0),
        session: Session = Depends(get_db)
    ):
    """
    Return products for gallery

    Args:
        num: int (1 ~ 12)

    Return:
        products: zip-file
    """
    gallery_items = random_read(session, num)

    return gallery_items

@router.get("/product/{uid}/download", response_class=StreamingResponse)
async def download_products(
        uid: UUID4,
        session: Session = Depends(get_db)
    ):
    """
    Return generated rounded squere pic like icon

    Args:
        uid: UUID

    Return:
        products: zip-file (contained two icons)
    """
    products = read_by_uuid(session, uid)

    if products:
        return StreamingResponse(products)
    else:
        raise Exception("Product is empty")
