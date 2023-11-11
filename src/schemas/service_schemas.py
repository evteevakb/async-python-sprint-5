"""Schemas for service endpoints"""
from pydantic import BaseModel


class ServicePing(BaseModel):
    """Response model for ping endpoint.

    Args:
        db (float): database ping time in seconds;
        storage (float): storage ping time in seconds.
    """
    db: float
    storage: float
