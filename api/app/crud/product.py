import os
import logging

from fastapi import File, UploadFile
from sqlalchemy.orm import Session
from sqlalchemy.sql.expression import func
from pydantic import UUID4, Field
from zipfile import ZipFile

from db import models

logger = logging.getLogger("genicons")

def create(
        db: Session,
        relation_id: UUID4,
        rs_icon: UploadFile = File(...),
        c_icon: UploadFile = File(...)
    ) -> bool:
    try:
        logger.info(f"{__name__}.{create.__name__}")

        db_product = models.Product(
                rounded_square_icon = rs_icon,
                circle_icon = c_icon,
                users_id = relation_id
                )
        db.add(db_product)
        db.commit()
        return True

    except Exception as e:
        logger.error(e)
        return False

def read_by_uuid(
        db: Session,
        uid: UUID4
    ):
    try:
        logger.info(f"{__name__}.{read_by_uuid.__name__}")

        user_data = db.query(models.Product).filter(models.Product.users_id == uid).first()

        with ZipFile(f'result_{uid}.zip', 'w') as zipObj:
            zipObj.write(user_data.rounded_square_icon)
            zipObj.write(user_data.circle_icon)

        return zipObj

    except Exception as e:
        logger.error(e)
        return False

    finally:
        os.remove(f'./result_{uid}.zip')

def random_read(
        db: Session,
        num: int = Field(..., min_num=3, max_num=12)
    ):
    try:
        logger.info(f"{__name__}.{random_read.__name__}")

        available_max = count(db)
        logger.info(f"Number of products: {available_max}")

        if num > available_max:
            num = available_max

        items = db.query(models.Product).order_by(func.rand()).limit(num).all()
        with ZipFile(f'./gallery.zip', 'w') as zipObj:
            for item in items:
                zipObj.write(item.rounded_square_icon)
                zipObj.write(item.circle_icon)

        return zipObj

    except Exception as e:
        logger.error(e)
        return False

    finally:
        os.remove(f'./gallery.zip')

'''
def update_by_id(db: Session, new_product: schemas.Product) -> bool:
    try:
        if not new_product.id:
            raise Exception('must be specify "id"')
        origin = db.query(models.Product).filter(models.Product.id == new_product.id).first()
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
        delete_db_product = db.query(models.Product).filter(models.Product.id == id).first()
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
'''

def count(
        db: Session
    ) -> int:
    try:
        logger.info(f"{__name__}.{count.__name__}")

        return db.query(models.Product).count()

    except Exception as e:
        logger.error(e)
        return False
