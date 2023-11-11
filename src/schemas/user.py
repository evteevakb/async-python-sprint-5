"""Request and response validation schemes for the Users model"""
from pydantic import BaseModel


class UserBase(BaseModel):
    """Base validation scheme for a user.

    Args:
       username (str): name of the user.
    """
    username: str
    password: str


class User(UserBase):
    pass


class UserCreate(UserBase):
    pass
    