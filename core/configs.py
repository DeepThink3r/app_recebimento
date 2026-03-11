from pydantic_settings import BaseSettings
from sqlalchemy.ext.declarative import declarative_base
from typing import ClassVar


class Settings(BaseSettings):
    API_V1_STR: str = '/api/v1'
    DB_URL: str = 'postgresql+asyncpg://recebimento:recebimento@localhost:5431/recebimento'
    DBBaseModel: ClassVar = declarative_base()

    SECRET_KEY: str = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

    class Config:
        case_sensitive = True


settings = Settings()