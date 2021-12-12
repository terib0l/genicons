from fastapi import FastAPI

from router import input, output

app = FastAPI()
app.include_router(input.router)
app.include_router(output.router)

from db.db_init import Base, ENGINE
Base.metadata.create_all(bind=ENGINE, checkfirst=False)

########################  Initialization  ########################
from sqlalchemy.orm import Session
from models import *
from uuid import uuid4
session = Session()
session.query(User).delete()
session.query(Product).delete()

sql_file = open(".sql", "r")
while file := sql_file.readline():
    img_name = file.split('/')[2]
    with open(file, "r") as img:
        session.add(User(uuid=uuid4(), img=img, img_name=img_name))
print(session.query(User).all())
###################################################################

############
# For test #
############
from fastapi import Request
from fastapi.responses import RedirectResponse
@app.get("/", response_class=RedirectResponse)
def index(request: Request):
    return RedirectResponse(request.url_for("index") + "docs")
