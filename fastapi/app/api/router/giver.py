import logging

from fastapi import APIRouter, Depends, Query, BackgroundTasks
from fastapi.responses import FileResponse
from sqlalchemy.ext.asyncio import AsyncSession
from pydantic import UUID4

from app.db.session import get_db
from app.api.crud.product import read_product, read_random_products
from app.api.crud.user import read_all_users
from app.api.module.utility import remove_file

logger = logging.getLogger("genicons").getChild("giver")

router = APIRouter()


@router.get("/all/users/fetch")
async def fetch_all_users(session: AsyncSession = Depends(get_db)):
    """
    Return data in user table

    Args:
    Return:

        dict: {id: img_name}
    """
    return await read_all_users(session)


@router.get("/product/fetch")
async def fetch_product(
    background: BackgroundTasks,
    product_id: UUID4 = Query(...),
    session: AsyncSession = Depends(get_db),
):
    """
    Return generated icons

    Args:
        product_id: UUID4

    Return:
        products: zip-file (contained two icons)
    """
    logger.info(fetch_product.__name__)

    product_path = f"./{product_id}.zip"
    await read_product(session, product_id, product_path)

    background.add_task(remove_file, path=product_path)

    return FileResponse(
        product_path,
        media_type="application/x-zip-compressed",
        headers={"Content-Disposition": f"attachment; filename={id}.zip"},
    )


@router.get("/gallery/fetch")
async def fetch_gallery(
    background: BackgroundTasks,
    gallery_num: int = Query(9, ge=1.0, le=12.0),
    session: AsyncSession = Depends(get_db),
):
    """
    Return products for gallery

    Args:
        num: query(int)

    Return:
        products: zip-file
    """
    gallery_path = "./gallery.zip"

    await read_random_products(session, gallery_num, gallery_path)

    background.add_task(remove_file, path=gallery_path)

    return FileResponse(
        gallery_path,
        media_type="application/x-zip-compressed",
        headers={"Content-Disposition": "attachment; filename=gallery.zip"},
    )
