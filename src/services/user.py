"""Contains a class that implements validation and work with the database for the ShortURLs model"""
from typing import Optional

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from services.base import RepositoryDB
from models.models import Users as UsersModel, Tokens as TokensModel
from schemas.user import TokenCreate, UserCreate


class RepositoryUsers(RepositoryDB[UsersModel, UserCreate]):
    async def read_by_username(self, database: AsyncSession, username: str) -> Optional[UsersModel]:
        statement = select(self._model).where(self._model.username == username)
        results = await database.execute(statement=statement)
        return results.scalar_one_or_none()


class RepositoryTokens(RepositoryDB[TokensModel, TokenCreate]):
    async def read_by_username(self, database: AsyncSession,
                               username: str) -> Optional[TokensModel]:
        statement = select(self._model).where(self._model.username == username)
        results = await database.execute(statement=statement)
        return results.scalar_one_or_none()

    async def read_by_token(self, database: AsyncSession, token: str) -> Optional[TokensModel]:
        statement = select(self._model).where(self._model.token == token)
        results = await database.execute(statement=statement)
        return results.scalar_one_or_none()


users_crud = RepositoryUsers(UsersModel)
token_crud = RepositoryTokens(TokensModel)
