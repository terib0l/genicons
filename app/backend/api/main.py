# Ref[progress bar]: https://stackoverflow.com/questions/64901945/how-to-send-a-progress-of-operation-in-a-fastapi-app

from fastapi import FastAPI, Request, BackgroundTasks, File, UploadFile
from fastapi.responses import FileResponse, RedirectResponse
from fastapi.middleware.cors import CORSMiddleware

import asyncio, aiofiles
from uuid import UUID
from typing import Dict

from module.ml import *
from module.schema import *
import db

app = FastAPI()

# Ref: https://fastapi.tiangolo.com/tutorial/bigger-applications/
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

jobs: Dict[UUID, GenerateStatus] = {}

@app.get("/", response_class=RedirectResponse)
def index(request: Request):
    return RedirectResponse(request.url_for("index") + "docs")

async def start_task(uid: UUID) -> None:
    queue = asyncio.Queue()
    asyncio.create_task(long_task(queue))

    while progress := await queue.get():
        jobs[uid].progress = progress

    jobs[uid].status = "complete"

# Ref: https://fastapi.tiangolo.com/tutorial/request-files/
# Ref: https://fastapi.tiangolo.com/tutorial/background-tasks/
# Ref: https://stackoverflow.com/questions/63580229/how-to-save-uploadfile-in-fastapi
@app.post("/icon/generate/")
async def generate(background: BackgroundTasks, file: UploadFile = File(...)):
    file_path = "./icon/" + file.filename
    async with aiofiles.open(file_path, 'wb') as save_file:
        content = await file.read()
        await save_file.write(content)
        await save_file.close()

    task = GenerateStatus()
    jobs[task.uid] = task
    background.add_task(start_task, task.uid)

    return {
            "message": "Start generating now!",
            "task_handle": task
    }

@app.get("/status/{uid}")
async def status(uid: UUID, request: Request):
    if jobs[uid].status == "complete":
        url = request.url_for("download") + "?uid={}".format(uid)
        jobs[uid].result = url

    return jobs[uid]

@app.get("/icon/download/", response_class=FileResponse)
async def download(uid: UUID):
    return {
            "rounded square": FileResponse("./icons/{}_rs.jpg".format(uid)),
            "circle": FileResponse("./icons/{}_c.jpg".format(uid))
    }
