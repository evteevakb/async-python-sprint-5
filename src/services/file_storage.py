"""Contains a class that implements validation and work with the database for the ShortURLs model"""
from typing import List

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from services.base import RepositoryDB
from models.models import Files as FilesModel
from schemas.file_storage import FileCreate


class RepositoryFiles(RepositoryDB[FilesModel, FileCreate]):
    async def read_many_by_username(self, database: AsyncSession,
                                    username: str) -> List[FilesModel]:
        statement = select(self._model).where(self._model.username == username)
        results = await database.execute(statement=statement)
        return results.scalars().all()


files_crud = RepositoryFiles(FilesModel)
