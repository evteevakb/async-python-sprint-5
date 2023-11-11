"""Database models"""
from sqlalchemy import Column, ForeignKey, String

from models.base import Base


class Users(Base):
    """Model of the 'users' table"""
    __tablename__ = 'users'
    username = Column(String, primary_key=True)
    password = Column(String, nullable=False)


class Tokens(Base):
    """Model of the 'tokens' table"""
    __tablename__ = 'tokens'
    username = Column(String, ForeignKey('users.username'), primary_key=True)
    token = Column(String, nullable=False, unique=True)


# class Files(Base):
#     """Model of the 'files' table"""
#     __tablename__ = 'files'
#     file_id = Column(Integer, primary_key=True)
#     filepath = Column(String, nullable=False, unique=True)
#     username = Column(String, ForeignKey('users.username'), nullable=False)
    