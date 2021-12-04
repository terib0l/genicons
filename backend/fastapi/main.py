from fastapi import FastAPI

from router import input, output

app = FastAPI()
app.include_router(input.router)
app.include_router(output.router)

from db.db_init import Base, ENGINE

Base.metadata.create_all(bind=ENGINE, checkfirst=False)

############
# For test #
############
from fastapi import Request
from fastapi.responses import RedirectResponse
@app.get("/", response_class=RedirectResponse)
def index(request: Request):
    return RedirectResponse(request.url_for("index") + "docs")
