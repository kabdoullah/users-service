import os
from datetime import date
from pathlib import Path
from pydantic_settings import BaseSettings, SettingsConfigDict

from pydantic import EmailStr


class AuthSettings(BaseSettings):
    APPLICATION: str = 'Auth Management System'
    WEBMASTER: str = 'bidigafadel@gmail.com'
    CREATED: date = date(2021, 11, 10)
    MAX_ATTEMPTS: int
    
    model_config = SettingsConfigDict(
        env_file=".env", env_ignore_empty=True, extra="ignore"
    )


class ServerSettings(BaseSettings):
    PRODUCTION_SERVER: str
    PROD_PORT: int
    DEVELOPMENT_SERVER: str
    DEV_PORT: int

    model_config = SettingsConfigDict(
        env_file=".env", env_ignore_empty=True, extra="ignore"
    )


class DBSettings(BaseSettings):
    
    DB_HOST: str 
    DB_PORT: int 
    DB_NAME: str 
    DB_USER: str 
    DB_PASSWORD: str 
    DB_URL: str
    
    model_config = SettingsConfigDict(
        env_file=".env", env_ignore_empty=True, extra="ignore"
    )


class EmailSettings(BaseSettings):
    MAIL_USERNAME: str
    MAIL_PASSWORD: str
    MAIL_FROM: EmailStr
    MAIL_PORT: int
    MAIL_SERVER: str
    MAIL_FROM_NAME: str

    model_config = SettingsConfigDict(
        env_file=".env", env_ignore_empty=True, extra="ignore"
    )



class RedisSettings(BaseSettings):
    REDIS_HOST: str | None = None
    REDIS_PORT: int | None = None
    REDIS_DB: int | None = None
    REDIS_PASSWORD: str | None = None

    model_config = SettingsConfigDict(
        env_file=".env", env_ignore_empty=True, extra="ignore"
    )



