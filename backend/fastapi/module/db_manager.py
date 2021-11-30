from sqlalchemy.orm import Session
from uuid import UUID

from conf.db_models import InitializeTable, ProductedTable

def create(db: Session, uuid: UUID, img: binary, img_name: str):
    Initialization = InitializeTable(user_id=uuid, img=img, img_name=img_name)
    db.add(Initialization)
    db.commit()
    db.refresh(Initialization)
    return Initialization

def read(db: Session, uuid: UUID):
    return db.query(InitializeTable).filter(InitializeTable.uuid == uuid).first()

def delete(db: Session, uuid: UUID):
    obj = db.query(InitializeTable).filter_by(InitializeTable.uuid == uuid).one()
    db.delete(obj)
    db.commit()
    return obj

def count(db: Session):
    return db.query(InitializeTable).count()

def read_rounded_square_pic(db: Session, uuid: UUID):
    pass

def read_circle_pic(db: Session, uuid: UUID):
    pass
