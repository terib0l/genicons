"""
    This is DB Function.
    Using MySQL.
    CRUD ... Create / Read / Update / Delete
"""
from fastapi import APIRouter

router = APIRouter(
        prefix="/works_db",
        tags=["db", "works"]
        )

@router.post("/create/")
def create():
    pass

@router.get("/read/")
def read():
    pass

@router.put("/update/")
def update():
    pass

@router.delete("/delete/")
def delete():
    pass
