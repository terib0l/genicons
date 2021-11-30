import os
BASE_DIR = os.getcwd()

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from starlette_validation_uploadfile import ValidateUploadFileMiddleware

from router import ui, db
from conf.db_config import Base, ENGINE

Base.metadata.create_all(bind=ENGINE, checkfirst=False)

app = FastAPI()

app.include_router(ui.router)
app.include_router(db.router)

app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*']
)

app.add_middleware(
    ValidateUploadFileMiddleware,
    app_path = [
        "/icon/generate/",
        "/pic/save",
    ],
    max_size = 16777216, # MySQL MEDIUMBLOB SIZE
    file_type = ["image/jpeg"]
)

############
# For test #
############
from fastapi import Request
from fastapi.responses import RedirectResponse
@app.get("/", response_class=RedirectResponse)
def index(request: Request):
    return RedirectResponse(request.url_for("index") + "docs")
