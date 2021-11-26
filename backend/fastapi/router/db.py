from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
import random

Base.metadata.create_all(bind=ENGINE)

router = APIRouter()

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/read/samples/")
def read_samples(order: int, db: Session = Depends(get_db)):
    sample_set = set()

    if order == 0:
        sample_set.add(range(1, 21))
    else:
        max = count(db)
        for _ in range(20):
            element = random.randint(1, max)
            sample_set.add(read_by_id(db, element).icon)

    return sample_set
