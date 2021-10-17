# Ref[progress bar]: https://stackoverflow.com/questions/64901945/how-to-send-a-progress-of-operation-in-a-fastapi-app

from fastapi import FastAPI, Request, BackgroundTasks, File, UploadFile
from fastapi.responses import FileResponse, RedirectResponse
from fastapi.middleware.cors import CORSMiddleware

import asyncio
from uuid import UUID, uuid4
from typing import Dict
from pydantic import BaseModel, Field

from module import ml

app = FastAPI()

# Ref: https://fastapi.tiangolo.com/tutorial/bigger-applications/
app.include_router(works.router)

# Ref: https://fastapi.tiangolo.com/tutorial/cors/
app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*']
)

class JobStatus(BaseModel):
    uid: UUID = Field(default_factory=uuid4)
    status: str = "in_progress"
    progress: int = 0
    result: str = ""

jobs: Dict[UUID, JobStatus] = {}

async def start_task(uid: UUID) -> None:
    queue = asyncio.Queue()
    asyncio.create_task(ml.long_task(queue))

    while progress := await queue.get():
        jobs[uid].progress = progress

    jobs[uid].status = "complete"

@app.get("/", response_class=RedirectResponse)
def index(request: Request):
    url = request.url_for("index")
    url += "docs"
    return RedirectResponse(url)

'''
def generate(background: BackgroundTasks, img: UploadFile = File(...)):
    # check img size
    if img:
        print(img.__dict__)
'''
@app.post("/icon/generate/")
def generate(background: BackgroundTasks):
    task = JobStatus()
    jobs[task.uid] = task
    # Ref: https://fastapi.tiangolo.com/tutorial/background-tasks/
    background.add_task(start_task, task.uid)

    return {
            "message": "Start generating now!",
            "task_handle": task
    }

@app.get("/status/{uid}")
def task_status(uid: UUID, request: Request):
    if jobs[uid].status == "complete":
        url = request.url_for("icon_download") + "?uid={}".format(uid)
        jobs[uid].result = url

    return jobs[uid]

@app.get("/icon/download/", response_class=FileResponse)
def icon_download(uid: UUID):
    return {
            "rounded square": FileResponse("./icons/{}_rs.jpg".format(uid)),
            "circle": FileResponse("./icons/{}_c.jpg".format(uid))
    }
