"""Request and response validation schemes for the Users and Token models"""
import uuid

from pydantic import BaseModel


class TokenBase(BaseModel):
    """Base validation scheme for tokens.

    Args:
       username (str): name of a user;
       token (str): user`s authentication token.
    """
    username: str
    token: str = uuid.uuid4()


class UserBase(BaseModel):
    """Base validation scheme for users.

    Args:
        username (str): name of a user;
        password (str): user`s password.
    """
    username: str
    password: str


class TokenCreate(TokenBase):
    """Validation scheme for token`s creation"""


class UserCreate(UserBase):
    """Validation scheme for user`s creation"""


class Token(TokenBase):
    """Validation scheme for token returned to a client"""
