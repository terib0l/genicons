from module.schema import ValidateULFileMiddleware, ValidateUploadFileMiddleware
from fastapi import FastAPI, Request, UploadFile, File 
from fastapi.responses import RedirectResponse

app = FastAPI()
app.add_middleware(ValidateULFileMiddleware, app_path="/gen/extended")
app.add_middleware(ValidateUploadFileMiddleware, app_path="/gen/starlette", max_size=100)

@app.get("/", response_class=RedirectResponse)
def index(request: Request):
    return request.url_for("index") + "docs"

@app.post("/gen/extended")
async def file(file: UploadFile = File(...)):
    """
    file_path = "./icon/" + file.filename
    async with aiofiles.open(file_path, 'wb') as save_file:
        content = await file.read()
        await save_file.write(content)
        await save_file.close()
    """

    return file.filename

@app.post("/gen/starlette")
async def file2(file: UploadFile = File(...)):
    """
    file_path = "./icon/" + file.filename
    async with aiofiles.open(file_path, 'wb') as save_file:
        content = await file.read()
        await save_file.write(content)
        await save_file.close()
    """

    return file.filename
