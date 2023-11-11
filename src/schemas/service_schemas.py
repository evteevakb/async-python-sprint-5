"""Schemas for service endpoints"""
from pydantic import BaseModel


class ServicePing(BaseModel):
    """Response model for ping endpoint.

    Args:
        status (str): status message.
    """
    status: str = 'OK'
