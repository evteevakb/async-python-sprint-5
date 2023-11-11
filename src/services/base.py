"""Contains mandatory methods for communication between the database and the application"""
from typing import Generic, Optional, Type, TypeVar

from fastapi.encoders import jsonable_encoder
from sqlalchemy import update
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from pydantic import BaseModel

from models.base import Base


ModelTypeT = TypeVar("ModelTypeT", bound=Base)
CreateSchemaTypeT = TypeVar("CreateSchemaTypeT", bound=BaseModel)


class Repository:
    """Agreement which methods will be created to implement CRUD"""
    async def create(self, database: AsyncSession, obj_in: CreateSchemaTypeT):
        """Create method"""
        raise NotImplementedError

    # async def read(self, database: AsyncSession, entity_id: int):
    #     """Read method"""
    #     raise NotImplementedError

    # async def delete(self, database: AsyncSession, entity_id: int):
    #     """Delete method"""
    #     raise NotImplementedError


class RepositoryDB(Repository, Generic[ModelTypeT, CreateSchemaTypeT]):
    """Base class for working with a database"""
    def __init__(self, model: Type[ModelTypeT]):
        self._model = model

    async def create(self, database: AsyncSession, obj_in: CreateSchemaTypeT) -> ModelTypeT:
        obj_in_data = jsonable_encoder(obj_in)
        db_obj = self._model(**obj_in_data)
        database.add(db_obj)
        await database.commit()
        await database.refresh(db_obj)
        return db_obj

    # async def read(self, database: AsyncSession, entity_id: int) -> Optional[ModelTypeT]:
    #     statement = select(self._model).where(self._model.id == entity_id)
    #     results = await database.execute(statement=statement)
    #     return results.scalar_one_or_none()

    # async def delete(self, database: AsyncSession, entity_id: int) -> None:
    #     statement = update(self._model).where(self._model.id == entity_id).values(active=False)
    #     await database.execute(statement=statement)
    #     await database.commit()