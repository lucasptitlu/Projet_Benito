from datetime import datetime

from enum import Enum

from fastapi import APIRouter
from pydantic import BaseModel


router = APIRouter()


class Status(Enum):
    UP = "UP"
    DEGRADED = "DEGRADED"
    DOWN = "DOWN"


class HealthStatus(BaseModel):
    comment: str
    status: Status = Status.UP
    version: str = "1.0"


@router.get("/", response_model=HealthStatus)
async def get_health_status():
    """

    Health Check Response from Server

    """

    return HealthStatus(comment=f"Healthy at {datetime.now()}")
