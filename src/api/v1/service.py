"""Contains service endpoints"""
from typing import Dict

from fastapi import APIRouter, Depends, HTTPException, status
from minio.error import MinioException, S3Error
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.sql import text

from core.logger import get_logger
from db.db import get_session
from schemas.service_schemas import ServicePing
from storage.storage import MinioClient


logger = get_logger(__name__)
router = APIRouter()


async def check_database(database: AsyncSession) -> bool:
    """Checks connection to a database.

    Args:
        database (AsyncSession): the database instance.

    Returns:
        bool: True if the database is connected otherwise False.
    """
    try:
        await database.execute(text('SELECT 1'))
        return True
    except OSError as exc:
        logger.error('Database is unavailable: %s', exc)
        return False


def check_storage() -> bool:
    """Checks connection to a S3 storage.

    Returns:
        bool: True if S3 storage is connected otherwise False.
    """
    try:
        MinioClient()
        return True
    except (MinioException, S3Error) as exc:
        logger.error('Storage is unavailable: %s', exc)
        return False


@router.get('/ping', response_model=ServicePing)
async def ping(database: AsyncSession = Depends(get_session)) -> Dict[str, str]:
    """Checks the status of additional services.

    Args:
        database (AsyncSession, optional): the database instance. Defaults to Depends(get_session).

    Raises:
        HTTPException: if any of the services is unavailable.

    Returns:
        Dict[str, str]: status message.
    """
    postgres_status = await check_database(database)
    minio_status = check_storage()
    if postgres_status and minio_status:
        return {"status": "OK"}
    details = {}
    if not postgres_status:
        details["postgres"] = "Connection error"
    if not minio_status:
        details["minio"] = "Connection error"
    raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail=f"Some services are unavailable: {details}",
        )
