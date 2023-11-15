"""Database models"""
from sqlalchemy import Column, ForeignKey, Integer, String

from core.config import app_settings
from models.base import Base


class Users(Base):
    """Model of the 'users' table"""
    __tablename__ = 'users'
    username = Column(String(app_settings.max_username_length), primary_key=True)
    password = Column(String(app_settings.max_password_length), nullable=False)


class Tokens(Base):
    """Model of the 'tokens' table"""
    __tablename__ = 'tokens'
    username = Column(String(app_settings.max_username_length), ForeignKey('users.username'),
                      primary_key=True)
    token = Column(String(app_settings.max_token_length), nullable=False, unique=True)


class Files(Base):
    """Model of the 'files' table"""
    __tablename__ = 'files'
    id = Column(Integer, primary_key=True)
    username = Column(String(app_settings.max_username_length), ForeignKey('users.username'),
                      nullable=False)
    filepath = Column(String(app_settings.max_filepath_length), nullable=False, unique=True)
