import logging

from fastapi import APIRouter, Depends, Path, BackgroundTasks, status
from fastapi.responses import FileResponse, JSONResponse
from sqlalchemy.orm import Session
from pydantic import UUID4

from app.db.session import get_db
from app.api.crud.product import read_by_uuid, random_read
from app.api.crud.user import all_read
from app.api.module.utility import remove_file

logger = logging.getLogger("genicons").getChild("giver")

router = APIRouter()


@router.get("/users/all/read")
def read_all(session: Session = Depends(get_db)):
    """
    Return data in user table

    Args:
    Return:

        dict: {id: img_name}
    """
    logger.info(read_all.__name__)

    return all_read(session)


@router.get("/gallery/{num}/download")
def get_gallery(
    background: BackgroundTasks,
    num: int = Path(..., ge=1.0, le=12.0),
    session: Session = Depends(get_db),
):
    """
    Return products for gallery

    Args:
        num: int (1 ~ 12)

    Return:
        products: zip-file
    """
    logger.info(get_gallery.__name__)
    gallery_path = "./gallery.zip"

    gallery = random_read(session, num)

    if gallery:
        background.add_task(remove_file, path=gallery_path)

        return FileResponse(
            gallery_path,
            media_type="application/x-zip-compressed",
            headers={"Content-Disposition": "attachment; filename=gallery.zip"},
        )
    else:
        return JSONResponse(
            status_code=status.HTTP_204_NO_CONTENT, content="No Content"
        )


@router.get("/product/{uid}/download")
def download_products(
    background: BackgroundTasks, uid: UUID4, session: Session = Depends(get_db)
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
    product_path = f"./{id}.zip"

    products = read_by_uuid(session, uid)

    if products:
        background.add_task(remove_file, path=product_path)

        return FileResponse(
            product_path,
            media_type="application/x-zip-compressed",
            headers={"Content-Disposition": f"attachment; filename={id}.zip"},
        )
    else:
        return JSONResponse(
            status_code=status.HTTP_204_NO_CONTENT, content="Product is empty"
        )
