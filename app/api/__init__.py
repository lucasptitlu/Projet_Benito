from fastapi import APIRouter
from app.api import health, database


api_router = APIRouter()


api_router.include_router(health.router, prefix="/health", tags=["health"])
api_router.include_router(database.router, prefix="/database", tags=["database"])
