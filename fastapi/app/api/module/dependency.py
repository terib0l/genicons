import logging
from enum import Enum
from typing import List

from fastapi import Request, File, Query, status, HTTPException
from fastapi.datastructures import UploadFile

logger = logging.getLogger("genicons")


class FileTypeName(str, Enum):
    jpeg = "image/jpeg"
    jpg = "image/jpeg"
    png = "image/png"
    gif = "image/gif"
    webp = "image/webp"
    pdf = "application/pdf"
    zip = "application/zip"
    txt = "text/plain"


# https://fastapi.tiangolo.com/advanced/advanced-dependencies/
class ValidateUploadFile:
    def __init__(
        self,
        max_size: int = Query(16777216),  # MIDIUMBLOB SIZE in MySQL
        file_type: List[FileTypeName] = Query(...),
    ):
        self.max_size = max_size
        self.file_type = file_type

    async def __call__(self, request: Request, img: UploadFile = File(...)):
        logger.info("validate UploadFile")
        # Check content-type
        form = await request.form()
        content_type = form[next(iter(form))].content_type
        if content_type not in self.file_type:
            logger.error(f"Unsupported Media Type: [{content_type}]")
            raise HTTPException(
                status_code=status.HTTP_415_UNSUPPORTED_MEDIA_TYPE,
                detail="Unsupported Media Type",
            )

        headers = request.headers
        if "content-length" not in headers:
            logger.error("Length Required")
            raise HTTPException(
                status_code=status.HTTP_411_LENGTH_REQUIRED, detail="Length Required"
            )
        # Check content-size
        content_length = int(headers["content-length"])
        if content_length > self.max_size:
            logger.error(
                f"Request Entity Too Large: {content_length} > {self.max_size}"
            )
            raise HTTPException(
                status_code=status.HTTP_413_REQUEST_ENTITY_TOO_LARGE,
                detail="Request Entity Too Large",
            )

        return img
