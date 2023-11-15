"""Request and response validation schemes for the Users and Token models"""
import uuid

from pydantic import BaseModel, Field

from core.config import app_settings


class TokenBase(BaseModel):
    """Base validation scheme for tokens.

    Args:
       username (str): name of a user;
       token (str): user`s authentication token.
    """
    username: str = Field(..., max_length=app_settings.max_username_length)
    token: str = Field(uuid.uuid4(), max_length=app_settings.max_token_length)


class UserBase(BaseModel):
    """Base validation scheme for users.

    Args:
        username (str): name of a user;
        password (str): user`s password.
    """
    username: str = Field(..., max_length=app_settings.max_username_length)
    password: str = Field(..., max_length=app_settings.max_password_length)


class TokenCreate(TokenBase):
    """Validation scheme for token`s creation"""


class UserCreate(UserBase):
    """Validation scheme for user`s creation"""


class Token(TokenBase):
    """Validation scheme for token returned to a client"""
