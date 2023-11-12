"""Contains API endpoints for file listing, uploading and downloading"""
import os
from typing import Annotated, Any, List

from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, Query
from fastapi import File as FAFile
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from api.v1.user import check_token
from db.db import get_session
from schemas.file_storage import File, FileCreate
from schemas.user import Token
from services.file_storage import files_crud
from storage.storage import MinioClient

from core.logger import get_logger

logger = get_logger(__name__)

router = APIRouter()
minio = MinioClient()


@router.get('/files', response_model=List[File])
async def get_files(database: AsyncSession = Depends(get_session),
                    user: Token = Depends(check_token)) -> Any:
    file_db = await files_crud.read_many_by_username(database=database, username=user.username)
    return [File(id=record.id, filepath=record.filepath) for record in file_db]



@router.post('/files/upload', status_code=status.HTTP_201_CREATED)
async def upload_file(database: AsyncSession = Depends(get_session),
                      user: Token = Depends(check_token),
                      filepath: Annotated[str | None, Query(pattern='^[A-Za-z]')] = None,
                      file: UploadFile = FAFile(...)) -> Any:
    """Uploads file into the storage.

    Args:
        database (AsyncSession, optional): database session. Defaults to Depends(get_session);
        user (Token, optional): user information including username and authentication token.
            Defaults to Depends(check_token);
        filepath (str, optional): path to the file in the storage. Defaults to None;
        file (UploadFile): file to be uploaded into the storage.

    Raises:
        HTTPException (406): if file with such filepath already exists.

    Returns:
        File: file information including record id and filepath in the storage.
    """
    if not filepath:
        filepath = os.path.join(user.username, file.filename)
    else:
        if os.path.basename(filepath): # file
            filepath = os.path.join(user.username, filepath)
        else:
            filepath = os.path.join(user.username, filepath, file.filename)
    try:
        file_db = await files_crud.create(database=database,
                                          obj_in=FileCreate(username=user.username,
                                                            filepath=filepath))
        await minio.upload_file(filepath=filepath, content=await file.read())
        return File(id=file_db.id, filepath=file_db.filepath)
    except IntegrityError as exc:
        raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE,
                            detail=f"File with filepath '{filepath}' already exists") from exc
