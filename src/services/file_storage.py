"""Contains a class that implements validation and work with the database for the ShortURLs model"""
from typing import List, Optional

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

    async def read_one_by_filepath(self, database: AsyncSession, username: str,
                                   filepath: str) -> Optional[FilesModel]:
        statement = select(self._model).where(self._model.filepath == filepath,
                                              self._model.username == username)
        results = await database.execute(statement=statement)
        return results.scalar_one_or_none()

    async def read_one_by_id(self, database: AsyncSession, username: str,
                             entity_id: int) -> Optional[FilesModel]:
        statement = select(self._model).where(self._model.id == entity_id,
                                              self._model.username == username)
        results = await database.execute(statement=statement)
        return results.scalar_one_or_none()


files_crud = RepositoryFiles(FilesModel)
