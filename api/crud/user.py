from sqlalchemy.orm import Session
from pydantic import UUID4, Field

from fastapi import UploadFile

import models, schemas

def create(db: Session, user: schemas.User) -> bool:
    try:
        db_user = models.User(
                id=user.id,
                img=user.img,
                img_name=user.img_name
                )
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
        return True
    except:
        return False

def read(db: Session, id: UUID4):
    try:
        return db.query(models.User).filter(models.User.id == id).first()
    except:
        return False

def all_read(db: Session):
    try:
        return db.query(models.User).all()
    except:
        return False

def update_img(db: Session, id: UUID4, img: UploadFile) -> bool:
    try:
        new_db_user = db.query(models.User).filter(models.User.id == id).first()
        new_db_user.img = img
        db.commit()
        return True
    except:
        return False

def update_img_name(db: Session, id: UUID4, img_name: str = Field(..., max_length=20)) -> bool:
    try:
        new_db_user = db.query(models.User).filter(models.User.id == id).first()
        new_db_user.img_name = img_name
        db.commit()
        return True
    except:
        return False

def delete(db: Session, id: UUID4) -> bool:
    try:
        delete_db_user = db.query(models.User).filter_by(models.User.id == id).first()
        db.delete(delete_db_user)
        db.commit()
        return True
    except:
        return False
