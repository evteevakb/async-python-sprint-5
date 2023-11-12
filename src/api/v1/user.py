"""Contains API endpoints for user registration and authentication"""
from typing import Any

import bcrypt
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from db.db import get_session
from schemas.user import Token, TokenCreate, UserCreate
from services.user import token_crud, users_crud


router = APIRouter()


async def check_token(token: str, database: AsyncSession = Depends(get_session)) -> None:
    """Checks authorization token of specific user.

    Args:
        token (str): user`s authorization token;
        database (AsyncSession, optional): database session. Defaults to Depends(get_session).

    Raises:
        HTTPException (401): if authorization token does not exists.

    Returns:
        Token: authorization info - username and its token.
    """
    token_db = await token_crud.read_by_token(database=database, token=token)
    if not token_db:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
    return Token(username=token_db.username, token=token_db.token)


@router.post("/register", status_code=status.HTTP_201_CREATED)
async def register_user(user: UserCreate, database: AsyncSession = Depends(get_session)) -> Any:
    """Registers a user. User`s password is stored in the database in a hashed form.

    Args:
        user (UserBase): user data containing username and password;
        database (AsyncSession, optional): database session. Defaults to Depends(get_session).

    Raises:
        HTTPException (406): if user with such username already exists.
    """
    try:
        user_create = UserCreate(username=user.username,
                                 password=bcrypt.hashpw(user.password.encode(), bcrypt.gensalt()))
        await users_crud.create(database=database, obj_in=user_create)
    except IntegrityError as exc:
        raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE,
                            detail=f"User with username '{user.username}' already exists") from exc


@router.post("/auth", response_model=Token, status_code=status.HTTP_200_OK)
async def authenticate_user(user: UserCreate, database: AsyncSession = Depends(get_session)) -> Any:
    """Generates authentication token for a specific user.

    Args:
        user (UserBase): user data containing username and password;
        database (AsyncSession, optional): database session. Defaults to Depends(get_session).

    Raises:
        HTTPException (404): if user with requested username does not exist;
        HTTPException (401): if password is incorrect.

    Returns:
        token data containing user`s username and token.
    """
    user_db = await users_crud.read_by_username(database=database, username=user.username)
    if user_db is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"User with username '{user.username}' not found")
    if not bcrypt.checkpw(user.password.encode(), user_db.password.encode()):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail='Password is incorrect')
    token_db = await token_crud.read_by_username(database=database, username=user.username)
    if token_db is None:
        token_db = await token_crud.create(database=database,
                                           obj_in=TokenCreate(username=user.username))
    return Token(username=token_db.username, token=token_db.token)
