import uvicorn
from fastapi import FastAPI

from app.router import router
from app.config import (
    PROJECT_NAME,
    VERSION,
    DEBUG,
)

app = FastAPI(title=PROJECT_NAME, version=VERSION, debug=DEBUG)
app.include_router(router, tags=["GENERATE"])

if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8080,
        reload=True,
    )
