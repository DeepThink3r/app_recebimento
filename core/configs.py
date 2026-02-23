from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    API_V1_STR: str = 'api/v1'
    DB_URL: str = 'postgresql+asyncpg://recebimento:recebimento@localhost:5431/recebimento'

    class Config:
        case_sensitive = True


settings = Settings()