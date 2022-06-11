import logging
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.base import api_router
from app.db.db_init import Base, ENGINE
from app.core.config import PROJECT_NAME, VERSION, DEBUG

Base.metadata.drop_all(ENGINE)
Base.metadata.create_all(bind=ENGINE, checkfirst=False)

logger = logging.getLogger("genicons")
logger.info("host=0.0.0.0, port=8888")

app = FastAPI(title=PROJECT_NAME, version=VERSION, debug=DEBUG)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://nuxt:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.include_router(api_router)
