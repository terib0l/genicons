from pydantic import BaseModel, Field
from uuid import UUID, uuid4

class GenerateStatus(BaseModel):
    uid: UUID = Field(default_factory=uuid4)
    status: str = "in_progress"
    progress: int = 0
    result: str = ""

# code Ref: https://github.com/encode/starlette/tree/master/starlette/middleware
# code Ref: https://github.com/tiangolo/fastapi/issues/362
# file_type Ref: https://developer.mozilla.org/ja/docs/Web/HTTP/Basics_of_HTTP/MIME_types/Common_types

import re
from typing import List
from starlette import status
from starlette.requests import Request
from starlette.types import ASGIApp, Scope, Send, Receive

def validation_error(status_code: int) -> ASGIApp:
    async def send_message(scope: Scope, receive: Receive, send: Send) -> None:
        await send(
            {
                "type": "http.response.start",
                "status": status_code
            }
        )
        await send({"type": "http.response.body", "body": b"", "more_body": False})

    return send_message

class ValidateUploadFileMiddleware:
    def __init__(self, app, app_path: str, max_size: int = 120000, file_type: List[str] = None) -> None:
        self.app = app
        self.app_path = re.compile(app_path)
        self.max_size = max_size
        self.file_type = file_type

    async def __call__(self, scope: Scope, receive: Receive, send: Send) -> None:
        if scope["type"] != "http" or scope["method"] != "POST":
            return await self.app(scope, receive, send)

        if not self.app_path.fullmatch(scope["path"]):
            return await self.app(scope, receive, send)

        request = Request(scope=scope, receive=receive)
        if self.file_type:
            form = await request.form()
            content_type = form[next(iter(form))].content_type
            if content_type not in self.file_type:
                return await validation_error(status.HTTP_415_UNSUPPORTED_MEDIA_TYPE)(scope, receive, send)

        if "content-length" not in request.headers:
            return await validation_error(status.HTTP_411_LENGTH_REQUIRED)(scope, receive, send)
        if int(request.headers["content-length"]) > self.max_size:
            return await validation_error(status.HTTP_413_REQUEST_ENTITY_TOO_LARGE)(scope, receive, send)

        return await self.app(scope, receive, send)

"""
from starlette.responses import Response
from starlette.middleware.base import BaseHTTPMiddleware, RequestResponseEndpoint

class ValidateULFileMiddleware(BaseHTTPMiddleware):
    def __init__(self, app, app_path: str, max_size: int = 120000, file_type: List[str] = None) -> None:
        super().__init__(app)
        self.app_path = re.compile(app_path)
        self.max_size = max_size
        self.file_type = file_type

    async def dispatch(self, request: Request, call_next: RequestResponseEndpoint) -> Response:
        if self.app_path.match(request.scope["path"]):
            if request.method == "POST":
                if self.file_type:
                    form = await request.form()
                    content_type = form[next(iter(form))].content_type
                    if content_type not in self.file_type:
                        return Response(status_code=status.HTTP_415_UNSUPPORTED_MEDIA_TYPE)

                if "content-length" not in request.headers:
                    return Response(status_code=status.HTTP_411_LENGTH_REQUIRED)
                if int(request.headers["content-length"]) > self.max_size:
                    return Response(status_code=status.HTTP_413_REQUEST_ENTITY_TOO_LARGE)

        response = await call_next(request)
        return response
"""
