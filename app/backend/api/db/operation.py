from sqlalchemy.orm import Session
from uuid import UUID

from .models import *

def create(db: Session, uuid: UUID, title: str, icon_url: str):
    db_sample = SampleTable(uuid=uuid, title=title, icon=icon_url)
    db.add(db_sample)
    db.commit()
    db.refresh(db_sample)
    return db_sample

def read_by_uuid(db: Session, uuid: UUID) -> None:
    return db.query(SampleTable).filter(SampleTable.uuid == uuid).first()

def read_by_id(db: Session, id: int):
    return db.query(SampleTable).filter(SampleTable.id == id).first()

def update_by_icon(db: Session, uuid: UUID, icon_url: str):
    obj = db.query(SampleTable).filter_by(uuid = uuid).one()
    obj.icon = icon_url
    db.add(obj)
    db.commit()

def update_by_title(db: Session, uuid: UUID, title: str):
    obj = db.query(SampleTable).filter_by(SampleTable.uuid == uuid).one()
    obj.title = title
    db.add(obj)
    db.commit()

def delete(db: Session, uuid: UUID):
    obj = db.query(SampleTable).filter_by(SampleTable.uuid == uuid).one()
    db.delete(obj)
    db.commit()
    return obj

def count(db: Session):
    return db.query(SampleTable).count()
