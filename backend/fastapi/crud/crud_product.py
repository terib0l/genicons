from uuid import UUID
from sqlalchemy.orm import Session

from fastapi import UploadFile, File

from models.product import ProductTable

def create(
        db: Session,
        uuid: UUID,
        rs_icon: UploadFile = File(...),
        c_icon: UploadFile = File(...)
    ):
    Initialization = ProductTable(
            id=uuid,
            rounded_square_icon=rs_icon,
            circle_icon=c_icon
            )

    db.add(Initialization)
    db.commit()
    db.refresh(Initialization)

    return Initialization

def read_rounded_square_pic(
        db: Session,
        uuid: UUID
    ):
    pass
    #return db.query(ProductTable).filter(ProductTable.uuid == uuid).first()

def read_circle_pic(
        db: Session,
        uuid: UUID
    ):
    pass
    #return db.query(ProductTable).filter(ProductTable.uuid == uuid).first()

def random_read(
        db: Session,
        num: int
    ):
    pass
    #return db.query(UserTable).filter(UserTable.uuid == uuid).first()

def update(
        db: Session,
        uuid: UUID
    ):
    pass

def delete(
        db: Session,
        uuid: UUID
    ):
    obj = db.query(ProductTable).filter_by(ProductTable.uuid == uuid).one()
    db.delete(obj)
    db.commit()
    return obj

def count(db: Session):
    return db.query(ProductTable).count()
