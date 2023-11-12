"""Contains a class that implements validation and work with the database for the ShortURLs model"""
from typing import Optional

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from services.base import RepositoryDB
from models.models import Users as UsersModel, Tokens as TokensModel
from schemas.user import TokenCreate, UserCreate


class RepositoryUsers(RepositoryDB[UsersModel, UserCreate]):
    """Validation and work with the database for the Users model"""
    async def read_by_username(self, database: AsyncSession, username: str) -> Optional[UsersModel]:
        """Searches a user by their username.

        Args:
            database (AsyncSession): database session;
            username (str): name of the user.

        Returns:
            Optional[UsersModel]: database record related to the requested user.
        """
        statement = select(self._model).where(self._model.username == username)
        results = await database.execute(statement=statement)
        return results.scalar_one_or_none()


class RepositoryTokens(RepositoryDB[TokensModel, TokenCreate]):
    """Validation and work with the database for the Token model"""
    async def read_by_username(self, database: AsyncSession,
                               username: str) -> Optional[TokensModel]:
        """Searches an authentication token for a specific user.

        Args:
            database (AsyncSession): database session;
            username (str): name of the user.

        Returns:
            Optional[TokensModel]: database record related to the requested user.
        """
        statement = select(self._model).where(self._model.username == username)
        results = await database.execute(statement=statement)
        return results.scalar_one_or_none()

    async def read_by_token(self, database: AsyncSession, token: str) -> Optional[TokensModel]:
        """Searches a user by their authentication token.

        Args:
            database (AsyncSession): database session;
            token (str): authentication token.

        Returns:
            Optional[TokensModel]: database record related to the requested token.
        """
        statement = select(self._model).where(self._model.token == token)
        results = await database.execute(statement=statement)
        return results.scalar_one_or_none()


users_crud = RepositoryUsers(UsersModel)
token_crud = RepositoryTokens(TokensModel)
