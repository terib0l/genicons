import logging

from fastapi import UploadFile
from sqlalchemy.orm import Session
from pydantic import UUID4, Field

from schemas.user import User
from db import models

logger = logging.getLogger("genicons")

# Using
def create(
        db: Session,
        user: User
    ) -> bool:
    try:
        db_user = models.User(
                id=user.id,
                img=user.img,
                img_name=user.img_name
                )
        db.add(db_user)
        db.commit()
        return True
    except Exception as e:
        logger.error(e)
        return False

def read(
        db: Session,
        id: UUID4
    ):
    try:
        return db.query(models.User).filter(models.User.id == id).first()
    except Exception as e:
        logger.error(e)
        return False

def all_read(
        db: Session
    ):
    try:
        return db.query(models.User).all()
    except Exception as e:
        logger.error(e)
        return False

def update_img(
        db: Session,
        id: UUID4,
        img: UploadFile
    ) -> bool:
    try:
        new_db_user = db.query(models.User).filter(models.User.id == id).first()
        new_db_user.img = img
        db.commit()
        return True
    except Exception as e:
        logger.error(e)
        return False

def update_img_name(
        db: Session,
        id: UUID4,
        img_name: str = Field(..., max_length=20)
    ) -> bool:
    try:
        new_db_user = db.query(models.User).filter(models.User.id == id).first()
        new_db_user.img_name = img_name
        db.commit()
        return True
    except Exception as e:
        logger.error(e)
        return False

def delete(
        db: Session,
        id: UUID4
    ) -> bool:
    try:
        delete_db_user = db.query(models.User).filter_by(models.User.id == id).first()
        db.delete(delete_db_user)
        db.commit()
        return True
    except Exception as e:
        logger.error(e)
        return False
