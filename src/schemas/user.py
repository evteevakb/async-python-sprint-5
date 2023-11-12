"""Request and response validation schemes for the Users model"""
import uuid

from pydantic import BaseModel


class TokenBase(BaseModel):
    username: str
    token: str = uuid.uuid4()


class UserBase(BaseModel):
    username: str
    password: str


class TokenCreate(TokenBase):
    pass


class UserCreate(UserBase):
    pass


class Token(TokenBase):
    pass
