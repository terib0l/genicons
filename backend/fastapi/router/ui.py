import aiofiles
from fastapi import APIRouter, Request, BackgroundTasks, File, UploadFile
from fastapi.responses import FileResponse
from uuid import UUID

from main import BASE_DIR
from module.schema import GenerateStatus
from module.utilities import jobs, start_task

router = APIRouter()

# Ref: https://fastapi.tiangolo.com/tutorial/request-files/
# Ref: https://fastapi.tiangolo.com/tutorial/background-tasks/
# Ref: https://stackoverflow.com/questions/63580229/how-to-save-uploadfile-in-fastapi
@router.post("/icon/generate/")
async def generate(background: BackgroundTasks, file: UploadFile = File(...)):
    """Start Generating pics
    
    * args
    file: jpeg

    * return
    message: str
    handle: dict (UUID contained)
    """
    file_name = file.filename
    file_path = f"{BASE_DIR}/icon/{file_name}"
    async with aiofiles.open(file_path, 'wb') as save_file:
        content = await file.read()
        await save_file.write(content)
        await save_file.close()

    task = GenerateStatus()
    jobs[task.uid] = task
    background.add_task(start_task, task.uid)

    return {
            "message": "Start Generating pic.",
            "handle": task
    }

@router.get("/status/{uid}")
async def status(request: Request, uid: UUID):
    """Return Handle

    * args
    uid: UUID

    * return
    handle: dict (UUID contained)
    """
    if jobs[uid].status == "complete":
        url = request.url_for("download") + "?uid={}".format(uid)
        jobs[uid].result = url

    return jobs[uid]

@router.get("/icon/download/", response_class=FileResponse)
async def download(uid: UUID):
    """Return generated pics like icon

    * args
    uid: UUID

    * return
    rs: jpeg (Rounded-Square pic)
    c: jpeg (Circle pic)
    """
    rounded_square_pic = f"{BASE_DIR}/icon/{uid}_rs.jpg"
    circle_pic = f"{BASE_DIR}/icon/{uid}_c.jpg"

    return {
            "rs": FileResponse(rounded_square_pic),
            "c": FileResponse(circle_pic)
    }
