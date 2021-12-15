import logging

from fastapi import FastAPI

from router import input, output
from db.db_init import Base, ENGINE

logger = logging.getLogger("genicons")

app = FastAPI()
app.include_router(input.router)
app.include_router(output.router)

logger.warning("Initialization database")
Base.metadata.drop_all(ENGINE)
Base.metadata.create_all(bind=ENGINE, checkfirst=False)

@app.get("/")
def index():
    logger.info("Index")
    return {"message": "Success!"}
