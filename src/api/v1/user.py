from typing import Any

import bcrypt
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from db.db import get_session
from schemas.user import UserBase, UserCreate
from services.user import users_crud

router = APIRouter()


@router.post("/register", status_code=status.HTTP_201_CREATED)
async def register_user(user: UserBase, database: AsyncSession = Depends(get_session)) -> Any:
    try:
        salt = bcrypt.gensalt()
        user_create = UserCreate(username=user.username,
                                 password=bcrypt.hashpw(user.password.encode(), salt),
                                 salt=salt)
        await users_crud.create(database=database, obj_in=user_create)
    except IntegrityError as exc:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail=f'User with username "{user.username}" already exists') from exc
