import logging

from fastapi import APIRouter, Depends, Path, BackgroundTasks
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session
from pydantic import UUID4
from starlette.responses import JSONResponse

from crud.product import read_by_uuid, random_read
from crud.user import all_read
from db.session import get_db
from module.utility import remove_file

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
    logger.info(read_all.__name__)

    try:
        return all_read(session)

    except Exception as e:
        logger.error(e)
        return JSONResponse(status_code=500, content="Internal Server Error")

@router.get("/gallery/{num}/download")
def get_gallery(
        background: BackgroundTasks,
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
    logger.info(get_gallery.__name__)
    gallery_path = './gallery.zip'

    try:
        gallery = random_read(session, num)

        if gallery:
            background.add_task(remove_file, path=gallery_path)

            return FileResponse(
                    gallery_path,
                    media_type="application/x-zip-compressed",
                    headers={
                        "Content-Disposition": "attachment; filename=gallery.zip"
                    }
            )
        else:
            return JSONResponse(status_code=204, content="No Content")

    except Exception as e:
        logger.error(e)
        return JSONResponse(status_code=500, content="Internal Server Error")

@router.get("/product/{uid}/download")
def download_products(
        background: BackgroundTasks,
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
    logger.info(download_products.__name__)

    id = str(uid)[:8]
    product_path = f'./{id}.zip'

    try:
        products = read_by_uuid(session, uid)

        if products:
            background.add_task(remove_file, path=product_path)

            return FileResponse(
                    product_path,
                    media_type="application/x-zip-compressed",
                    headers={
                        "Content-Disposition": f"attachment; filename={id}.zip"
                    }
            )
        else:
            return JSONResponse(status_code=204, content="Product is empty")

    except Exception as e:
        logger.error(e)
        return JSONResponse(status_code=500, content="Internal Server Error")
