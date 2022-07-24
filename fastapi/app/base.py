from app.api.router import giver, generator, management
from fastapi import APIRouter

api_router = APIRouter()
api_router.include_router(giver.router, tags=["GIVER"])
api_router.include_router(generator.router, tags=["GENERATOR"])
api_router.include_router(management.router, tags=["MANAGEMENT"])
