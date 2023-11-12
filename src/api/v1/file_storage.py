from typing import Any

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from api.v1.user import check_token
from db.db import get_session
from schemas.user import Token

router = APIRouter()


@router.get('/files')
async def get_files(database: AsyncSession = Depends(get_session),
                    user: Token = Depends(check_token)) -> Any:
    return {'authentication' : 'OK'}
