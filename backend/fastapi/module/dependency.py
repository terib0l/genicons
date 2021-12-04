from enum import Enum
from typing import List

from fastapi import Request, File, status
from fastapi.param_functions import Query
from fastapi.responses import PlainTextResponse
from fastapi.datastructures import UploadFile
from sqlalchemy.orm import Session

# Dependency
def get_db():
    session = Session()
    try:
        yield session
    except:
        session.rollback()
        raise
    finally:
        session.close()

_unsupported_media_type = PlainTextResponse("Unsupported Media Type", status.HTTP_415_UNSUPPORTED_MEDIA_TYPE)
_length_required = PlainTextResponse("Length Required", status.HTTP_411_LENGTH_REQUIRED)
_request_entity_too_large = PlainTextResponse("Request Entity Too Large", status.HTTP_413_REQUEST_ENTITY_TOO_LARGE)

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
            max_size: int = Query(16777216), # MIDIUMBLOB SIZE in MySQL
            file_type: List[FileTypeName] = Query(...)
        ):
        self.max_size = max_size
        self.file_type = file_type

    def __call__(self, request: Request, img: UploadFile = File(...)):
        # Check content-type
        form = request.form()
        content_type = form[next(iter(form))].content_type
        if content_type not in self.file_type:
            return _unsupported_media_type

        headers = request.headers
        if "content-length" not in headers:
            return _length_required
        # Check content-size
        if int(headers["content-length"]) > self.max_size:
            return _request_entity_too_large

        return img
