import os
BASE_DIR = os.getcwd()

from fastapi import FastAPI

from router import input, output
from conf.db_config import Base, ENGINE

Base.metadata.create_all(bind=ENGINE, checkfirst=False)

app = FastAPI()

app.include_router(input.router)
app.include_router(output.router)

############
# For test #
############
from fastapi import Request
from fastapi.responses import RedirectResponse
@app.get("/", response_class=RedirectResponse)
def index(request: Request):
    return RedirectResponse(request.url_for("index") + "docs")
