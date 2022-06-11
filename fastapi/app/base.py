from app.api.router import giver, generator
from fastapi import APIRouter

api_router = APIRouter()
api_router.include_router(giver.router, tags=["giver"])
api_router.include_router(generator.router, tags=["generator"])
