import logging

from fastapi import FastAPI

logger = logging.getLogger("genicons")
logger.info("host=0.0.0.0, port=8888")

app = FastAPI()

from router import generator, giver
app.include_router(generator.router)
app.include_router(giver.router)

from db.db_init import Base, ENGINE
Base.metadata.drop_all(ENGINE)
Base.metadata.create_all(bind=ENGINE, checkfirst=False)
