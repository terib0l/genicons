from fastapi import FastAPI, Request, BackgroundTasks, File, UploadFile
from fastapi.responses import FileResponse, RedirectResponse
from fastapi.middleware.cors import CORSMiddleware
from module import *
from db import works, auths
from ml import model

app = FastAPI()

app.include_router(works.router)
app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*']
)

@app.get("/")
def index():
    pass

@app.post("/generate/")
def generate(background: BackgroundTasks, img: UploadFile = File(...)):
    # check img size

    background.add_task(model.style_transfer, img)
    return {"message": "Generating now!"}

@app.get("/status/")
def generate_status(request: Request):
    # confirm status -> return progress variable

    if progress < 100:
        return {
            "message": "In progress",
            "progress": progress
        }
    else:
        url = request.url_for("icon_download")
        return RedirectResponse(url=url, status_code=200)

@app.get("/download/", response_class=FileResponse)
def icon_download():
    return {
            "rounded square": FileResponse("./icons/****_rs.jpg"),
            "circle": FileResponse("./icons/****_c.jpg")
    }
