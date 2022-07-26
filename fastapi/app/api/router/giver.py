import logging
from pydantic import UUID4
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import APIRouter, Depends, Query, BackgroundTasks, status
from fastapi.responses import FileResponse, JSONResponse

from app.db.session import get_db
from app.api.crud.product import read_product, read_random_products
from app.api.crud.user import read_product_ids
from app.api.module.utility import remove_file

logger = logging.getLogger("genicons").getChild("giver")

router = APIRouter()


@router.get("/fetch/product/ids")
async def fetch_product_ids(
    user_id: int = Query(...),
    session: AsyncSession = Depends(get_db),
):
    """
    Return data in user table

    Args:

        user_id: query(int)

    Return:

        list: [{name, id, premium, email}, ...]
    """
    return await read_product_ids(session, user_id)


@router.get("/fetch/product")
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
    product_path = f"./{product_id}.zip"
    res = await read_product(session, product_id, product_path)

    if not res:
        return JSONResponse(
            status_code=status.HTTP_204_NO_CONTENT, content="No products yet"
        )

    background.add_task(remove_file, path=product_path)

    return FileResponse(
        product_path,
        media_type="application/x-zip-compressed",
        headers={"Content-Disposition": f"attachment; filename={product_id}.zip"},
    )


@router.get("/fetch/gallery")
async def fetch_gallery(
    background: BackgroundTasks,
    gallery_num: int = Query(9, ge=1.0, le=12.0),
    session: AsyncSession = Depends(get_db),
):
    """
    Return products for gallery

    Args:

        gallery_num: query(int)

    Return:

        products: zip-file
    """
    gallery_path = "./gallery.zip"
    res = await read_random_products(session, gallery_num, gallery_path)

    if not res:
        return JSONResponse(
            status_code=status.HTTP_204_NO_CONTENT, content="No products yet"
        )

    background.add_task(remove_file, path=gallery_path)

    return FileResponse(
        gallery_path,
        media_type="application/x-zip-compressed",
        headers={"Content-Disposition": "attachment; filename=gallery.zip"},
    )
