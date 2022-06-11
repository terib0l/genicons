import os
import logging
import zipfile

from fastapi import File, UploadFile, Query
from sqlalchemy.orm import Session
from sqlalchemy.sql.expression import func
from pydantic import UUID4

from app.db import models
from app.api.module.utility import remove_file

logger = logging.getLogger("genicons")


def create(
    db: Session,
    relation_id: UUID4,
    rs_icon: UploadFile = File(...),
    c_icon: UploadFile = File(...),
) -> bool:
    try:
        logger.info(f"{__name__}.{create.__name__}")

        db_product = models.Product(
            rounded_square_icon=rs_icon, circle_icon=c_icon, users_id=relation_id
        )
        db.add(db_product)
        db.commit()
        return True

    except Exception as e:
        logger.error(e)
        return False


def read_by_uuid(db: Session, uid: UUID4) -> bool:
    id = str(uid)[:8]
    handle_jpg = [f"./rs_{id}.jpg", f"./c_{id}.jpg"]

    try:
        logger.info(f"{__name__}.{read_by_uuid.__name__}")

        user_data = (
            db.query(models.Product).filter(models.Product.users_id == uid).first()
        )
        if not user_data:
            raise Exception("No Products data by its uuid")

        # First, make img-files
        with open(handle_jpg[0], "wb") as rs_file:
            rs_file.write(user_data.rounded_square_icon)
        with open(handle_jpg[1], "wb") as c_file:
            c_file.write(user_data.circle_icon)

        # Second, make zip-file contained img-files
        with zipfile.ZipFile(f"./{id}.zip", "w") as zipObj:
            [zipObj.write(jpg) for jpg in handle_jpg]

        return True

    except Exception as e:
        logger.error(e)
        return False

    finally:
        remove_file(paths=handle_jpg)


def random_read(db: Session, num: int = Query(..., min_num=1, max_num=12)) -> bool:
    logger.info(f"{__name__}.{random_read.__name__}")

    available_max = count(db)
    logger.info(f"Number of products: {available_max}")

    if not available_max:
        return False

    if num > available_max:
        num = available_max

    handle_jpg = []
    for i in range(num):
        handle_jpg.append([f"./rs_{i+1}.jpg", f"./c_{i+1}.jpg"])

    try:
        user_datas = db.query(models.Product).order_by(func.rand()).limit(num).all()

        # First, make img-files
        for i, user_data in enumerate(user_datas):
            with open(handle_jpg[i][0], "wb") as rs_file:
                rs_file.write(user_data.rounded_square_icon)
            with open(handle_jpg[i][1], "wb") as c_file:
                c_file.write(user_data.circle_icon)
        logger.info(f"{random_read.__name__} {os.listdir()}")

        # Second, make zip-file contained img-files
        with zipfile.ZipFile("./gallery.zip", "w") as zipObj:
            for jpg_paths in handle_jpg:
                for jpg in jpg_paths:
                    if os.path.isfile(jpg):
                        zipObj.write(jpg)

        return True

    except Exception as e:
        logger.error(e)
        return False

    finally:
        for jpg_paths in handle_jpg:
            remove_file(paths=jpg_paths)


"""
def update_by_id(db: Session, new_product: schemas.Product) -> bool:
    try:
        if not new_product.id:
            raise Exception('must be specify "id"')
        origin = \
            db.query(models.Product).filter(models.Product.id == new_product.id).first()
        origin.rounded_square_icon = new_product.rounded_square_icon
        origin.circle_icon = new_product.circle_icon
        db.commit()
        return True
    except:
        return False

def update_by_uuid(db: Session, uuid: UUID4, new_product: schemas.Product) -> bool:
    try:
        origin = db.query(models.User).filter(models.User.id == uuid).first()
        origin.products = [
                new_product.rounded_square_icon,
                new_product.circle_icon
            ]
        db.commit()
        return True
    except:
        return False

def delete_by_id(db: Session, id: int) -> bool:
    try:
        delete_db_product = \
            db.query(models.Product).filter(models.Product.id == id).first()
        db.delete(delete_db_product)
        db.commit()
        return True
    except:
        return False

def delete_by_uuid(db: Session, uuid: UUID4) -> bool:
    try:
        delete_db_user = db.query(models.User).filter(models.User.id == uuid).first()
        db.delete(delete_db_user.products)
        db.commit()
        return True
    except:
        return False
"""


def count(db: Session) -> int:
    try:
        logger.info(f"{__name__}.{count.__name__}")

        return db.query(models.Product).count()

    except Exception as e:
        logger.error(e)
        return False
