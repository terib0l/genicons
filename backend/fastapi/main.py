import os
BASE_DIR = os.getcwd()

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from router import ui, db
from module.middleware import ValidateUploadFileMiddleware

app = FastAPI()

# Ref: https://fastapi.tiangolo.com/tutorial/bigger-applications/
app.include_router(ui.router)
app.include_router(db.router)

# Ref: https://fastapi.tiangolo.com/tutorial/cors/
app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*']
)

app.add_middleware(
    ValidateUploadFileMiddleware,
    app_path = "/icon/generate/",
    max_size = 120000,
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
