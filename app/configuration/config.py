import os
from datetime import date
from pathlib import Path
from pydantic_settings import BaseSettings
from pydantic import EmailStr



class AuthSettings(BaseSettings):
    APPLICATION: str = 'Auth Management System'
    WEBMASTER: str = 'bidigafadel@gmail.com'
    CREATED: date = date(2021, 11, 10)

class ServerSettings(BaseSettings):
    PRODUCTION_SERVER: str
    PROD_PORT: int
    DEVELOPMENT_SERVER: str
    DEV_PORT: int

    class Config:
        env_file = Path(os.getcwd()) / 'configuration' / 'erp_settings.properties'

class DBSettings(BaseSettings):
    DB_HOST: str
    DB_PORT: int
    DB_NAME: str
    DB_USER: str
    DB_PASSWORD: str

    class Config:
        env_file = Path(os.getcwd()) / 'configuration' / 'db_settings.properties'



class EmailSettings(BaseSettings):
    MAIL_USERNAME: str
    MAIL_PASSWORD: str
    MAIL_FROM: EmailStr
    MAIL_PORT: int
    MAIL_SERVER: str
    MAIL_FROM_NAME: str

    class Config:
        env_file = Path(os.getcwd()) / 'configuration' / 'email_settings.properties'


