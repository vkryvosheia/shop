import logging

import sqlalchemy
from fastapi import APIRouter, Response, status
from pydantic import BaseModel
from sqlalchemy.exc import SQLAlchemyError

from app.api.deps import DbSession

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/health", tags=["health"])


class HealthResponse(BaseModel):
    status: str
    database: str


@router.get("", response_model=HealthResponse)
def health_check(db: DbSession, response: Response):
    try:
        db.execute(sqlalchemy.text("SELECT 1"))
        return HealthResponse(status="ok", database="ok")
    except SQLAlchemyError:
        logger.exception("Database health check failed")
        response.status_code = status.HTTP_503_SERVICE_UNAVAILABLE
        return HealthResponse(status="error", database="unavailable")
