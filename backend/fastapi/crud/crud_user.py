from sqlalchemy.orm import Session
from uuid import UUID

from fastapi import UploadFile, File

from models.user import UserTable

def create(
        db: Session,
        uuid: UUID,
        img_name: str,
        img: UploadFile = File(...)
    ):
    Initialization = UserTable(
            user_id=uuid,
            img=img,
            img_name=img_name
            )

    db.add(Initialization)
    db.commit()
    db.refresh(Initialization)

    return Initialization

def read(
        db: Session,
        uuid: UUID
    ):
    return db.query(UserTable).filter(UserTable.uuid == uuid).first()

def update(
        db: Session,
        uuid: UUID
    ):
    pass

def delete(
        db: Session,
        uuid: UUID
    ):
    obj = db.query(UserTable).filter_by(UserTable.uuid == uuid).one()
    db.delete(obj)
    db.commit()
    return obj
