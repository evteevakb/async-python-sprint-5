"""Contains service endpoints"""
import time
from typing import Dict

from fastapi import APIRouter, Depends, HTTPException, status
from miniopy_async.error import MinioException, S3Error
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.sql import text

from db.db import get_session
from schemas.service import ServicePing
from storage.storage import MinioClient


router = APIRouter()


async def ping_database(database: AsyncSession) -> Dict[str, float]:
    """Checks connection to a database.

    Args:
        database (AsyncSession): the database session.

    Raises:
        HTTPException: if database is unavailable.

    Returns:
        Dict[str, float]: database ping time in seconds.
    """
    try:
        start_time = time.time()
        await database.execute(text('SELECT 1'))
        end_time = time.time()
        return {'db': f'{round((end_time - start_time), 2)}'}
    except OSError as exc:
        raise HTTPException(status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                            detail="Database is unavailable") from exc


async def ping_storage() -> Dict[str, float]:
    """Checks connection to a S3 storage.

    Raises:
        HTTPException: if storage is unavailable.

    Returns:
        Dict[str, float]: storage ping time in seconds.
    """
    try:
        start_time = time.time()
        await MinioClient().check_bucket()
        end_time = time.time()
        return {'storage': f'{round((end_time - start_time), 2)}'}
    except (MinioException, S3Error) as exc:
        raise HTTPException(status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                            detail="Storage is unavailable") from exc


@router.get('/ping', response_model=ServicePing)
async def ping(database: AsyncSession = Depends(get_session)) -> Dict[str, float]:
    """Checks the status of additional services.

    Args:
        database (AsyncSession, optional): the database session. Defaults to Depends(get_session).

    Raises:
        HTTPException: if any of the services is unavailable.

    Returns:
        Dict[str, float]: dictionary with ping time in seconds for each service.
    """
    try:
        database_ping_time = await ping_database(database)
        storage_ping_time = await ping_storage()
        return database_ping_time | storage_ping_time
    except HTTPException as exc:
        raise HTTPException(status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                            detail=exc.detail) from exc
