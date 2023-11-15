"""App configuration"""
from pydantic import PostgresDsn
from pydantic_settings import BaseSettings


class AppSettings(BaseSettings):
    """Contains application settings"""
    app_title: str = 'URL Shortener'
    database_dsn: PostgresDsn
    database_echo: bool = True
    max_username_length: int = 16
    max_filepath_length: int = 256
    max_token_length: int = 36 # token length of uuid4
    max_password_length: int = 72 # max bcrypt password hash length

    class Config:
        """Application environment variables"""
        env_file = '.env.app'


app_settings = AppSettings()
 