import os

from sqlalchemy.orm import Session
from sqlalchemy.sql.expression import func
from pydantic import UUID4, Field
from zipfile import ZipFile

import models, schemas

def create(db: Session, product: schemas.Product) -> bool:
    try:
        db_product = models.User(
                products=[product.rounded_square_icon, product.circle_icon]
                )
        db.add(db_product)
        db.commit()
        db.refresh(db_product)
        return True
    except:
        return False

def all_read(db: Session):
    try:
        raise Exception("No implementation")
        #return db.query(models.Product).all()
    except:
        return False

def read_by_id(db: Session, id: int):
    try:
        return db.query(models.Product).filter(models.Product.id == id).first()
    except:
        return False

def read_by_uuid(db: Session, uuid: UUID4) -> ZipFile:
    try:
        user = db.query(models.User).filter(models.User.uuid == uuid).first()

        with ZipFile('tmp.zip', 'w') as zipObj:
            zipObj.write(user.products.rounded_square_icon)
            zipObj.write(user.products.circle_icon)

        return zipObj
    except:
        raise Exception('read_by_uuid is error')
    finally:
        os.remove('./tmp.zip')

def random_read(db: Session, num: int = Field(..., max_num=20, min_num=10)):
    try:
        max = count(db)
        if num > max:
            num = max
        return db.query(models.Product).order_by(func.rand()).limit(num).all()
    except:
        return False

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

def count(db: Session) -> int:
    return db.query(models.Product).count()
