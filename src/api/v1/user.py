from typing import Any

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from db.db import get_session
from schemas.user import UserCreate
from services.user import users_crud

router = APIRouter()


@router.post("/register", status_code=status.HTTP_201_CREATED)
async def register_user(user: UserCreate, database: AsyncSession = Depends(get_session)) -> Any:
    try:
        await users_crud.create(database=database, obj_in=user)
    except IntegrityError as exc:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail=f'User with username "{user.username}" already exists') from exc
