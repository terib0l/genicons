import logging

from sqlalchemy.orm import Session
from pydantic import UUID4

from app.db import models
from app.api.schema.user import User

logger = logging.getLogger("genicons")


def create(db: Session, user: User) -> bool:
    logger.info(f"{__name__}.{create.__name__}")

    try:
        db_user = models.User(
            id=user.id, name=user.name, email=user.email, premium=False
        )
        db.add(db_user)
        db.commit()
        return True

    except Exception as e:
        logger.error(e)
        return False


def read(db: Session, id: UUID4):
    logger.info(f"{__name__}.{read.__name__}")

    try:
        return db.query(models.User).filter(models.User.id == id).first()

    except Exception as e:
        logger.error(e)
        return False


def all_read(db: Session):
    logger.info(f"{__name__}.{all_read.__name__}")

    try:
        ret = {}
        datas = db.query(models.User).all()
        if datas:
            for data in datas:
                ret[data.id] = data.img_name
        return ret

    except Exception as e:
        logger.error(e)
        return False


"""
def update_img(
        db: Session,
        id: UUID4,
        img: UploadFile = File(...)
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
"""
