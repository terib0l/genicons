"""
    This is DB Function.
    Using MySQL.
    CRUD ... Create / Read / Update / Delete
"""
from fastapi import APIRouter

router = APIRouter(
        prefix="/auths_db",
        tags=["db", "auths"]
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

