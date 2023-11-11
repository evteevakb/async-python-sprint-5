"""Request and response validation schemes for the Users model"""
import uuid

from pydantic import BaseModel


class UserBase(BaseModel):
    """Base validation scheme for a user.

    Args:
       username (str): name of the user.
    """
    username: str
    password: str


class UserCreate(UserBase):
    pass


class TokenBase(BaseModel):
    username: str
    token: str = uuid.uuid4()


class TokenCreate(TokenBase):
    pass


class Token(TokenBase):
    pass
