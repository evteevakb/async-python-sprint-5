"""Contains a class that implements validation and work with the database for the ShortURLs model"""
# from typing import Optional

# from sqlalchemy.ext.asyncio import AsyncSession
# from sqlalchemy.future import select

from services.base import RepositoryDB
from models.models import Files as FilesModel
from schemas.file_storage import FileCreate


class RepositoryFiles(RepositoryDB[FilesModel, FileCreate]):
    pass


files_crud = RepositoryFiles(FilesModel)
