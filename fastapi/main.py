import logging
import uvicorn
from pathlib import Path

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.base import api_router
from app.core.config import PROJECT_NAME, VERSION, DEBUG

logger = logging.getLogger("genicons")
logger.info("http://localhost:8888/docs")

app = FastAPI(title=PROJECT_NAME, version=VERSION, debug=DEBUG)
app.add_middleware(
    CORSMiddleware,
    # allow_origins=["http://nuxt:3000"],
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.include_router(api_router)


@app.on_event("startup")
def startup_event():
    pass


@app.get("/")
def index():
    return "success"


if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8888,
        reload=True,
        log_config=str(Path(Path(__file__).resolve().parent, "log", "logging.yaml")),
    )
