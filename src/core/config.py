"""App configuration"""
from pydantic import PostgresDsn
from pydantic_settings import BaseSettings


class AppSettings(BaseSettings):
    """Contains application settings"""
    app_title: str = 'URL Shortener'
    database_dsn: PostgresDsn
    database_echo: bool = True

    class Config:
        """Application environment variables"""
        env_file = '.env.app'


app_settings = AppSettings()
 