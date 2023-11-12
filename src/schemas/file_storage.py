"""Request and response validation schemes for the Files model"""
from pydantic import BaseModel


class FileBase(BaseModel):
    pass


class FileCreate(FileBase):
    username: str
    filepath: str


class File(FileBase):
    id: int
    filepath: str
    