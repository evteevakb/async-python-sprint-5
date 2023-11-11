from fastapi import FastAPI
from fastapi.responses import ORJSONResponse

from api.v1.base import api_router
from core.config import app_settings


app = FastAPI(
    title=app_settings.app_title,
    docs_url='/api/openapi',
    openapi_url='/api/openapi.json',
    # replace the standard JSON serializer with a faster version written in Rust for optimization
    default_response_class=ORJSONResponse,
)

app.include_router(api_router, prefix='/api/v1')
