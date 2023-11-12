"""Request and response validation schemes for the Files model"""
from pydantic import BaseModel


class FileBase(BaseModel):
    """Base validation scheme for files"""


class FileCreate(FileBase):
    """Validation scheme for file`s creation.

    Args:
       username (str): name of a user;
       filepath (str): path to a file in the storage.
    """
    username: str
    filepath: str


class File(FileBase):
    """Validation scheme for a file returned to a client.

    Args:
        id (int): unique identifier of the file;
        filepath (str): path to a file in the storage.
    """
    id: int
    filepath: str
    