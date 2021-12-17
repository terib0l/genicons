import logging

from fastapi import APIRouter, Depends, Path
from fastapi.responses import StreamingResponse
from sqlalchemy.orm import Session
from pydantic import UUID4
from starlette.responses import JSONResponse

from crud.product import read_by_uuid, random_read
from crud.user import all_read
from db.session import get_db

logger = logging.getLogger("genicons")

router = APIRouter(
        tags=["giver"]
        )

@router.get("/users/all/read")
def read_all(
        session: Session = Depends(get_db)
    ):
    """
    Return data in user table

    Args:
    Return:

        dict: {id: img_name}
    """
    try:
        logger.info(read_all.__name__)

        return all_read(session)

    except Exception as e:
        logger.error(e)
        return JSONResponse(status_code=500, content="Internal Server Error")

@router.get("/gallery/{num}/download")
def gallery(
        num: int = Path(..., ge=1.0, le=12.0),
        session: Session = Depends(get_db)
    ):
    """
    Return products for gallery

    Args:
        num: int (1 ~ 12)

    Return:
        products: zip-file
    """
    try:
        logger.info(gallery.__name__)

        gallery_items = random_read(session, num)

        if gallery_items:
            return StreamingResponse(gallery_items)
        else:
            raise Exception("Products is empty")

    except Exception as e:
        logger.error(e)
        return JSONResponse(status_code=500, content="Internal Server Error")

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
    try:
        logger.info(download_products.__name__)

        products = read_by_uuid(session, uid)

        if products:
            return StreamingResponse(products)
        else:
            raise Exception("Product is empty")

    except Exception as e:
        logger.error(e)
        return JSONResponse(status_code=500, content="Internal Server Error")
