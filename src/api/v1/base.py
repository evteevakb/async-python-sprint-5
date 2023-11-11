"""Contains router with handlers"""
from fastapi import APIRouter

from api.v1.file_storage import router
from api.v1.service import router as service_router


api_router = APIRouter()
api_router.include_router(service_router, prefix='/service', tags=['service'])
api_router.include_router(router, prefix='/file_storage', tags=['file_storage'])
