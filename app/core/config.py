
from functools import lru_cache

from pydantic import SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict
from sqlalchemy.engine import URL


class Settings(BaseSettings):

    APP_NAME        : str = "FastAPI Enterprise API"
    APP_ENV         : str = "development"
    DEBUG           : bool = False

    DB_HOST         : str = "localhost"
    DB_PORT         : int = 5432
    DB_NAME         : str = "ecommerce_db"
    DB_USER         : str = "postgres"
    DB_PASSWORD     : SecretStr

    DB_POOL_SIZE    : int = 10
    DB_MAX_OVERFLOW : int = 10
    DB_POOL_TIMEOUT : int = 30

    SECRET_KEY      : SecretStr

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=True,
        extra="ignore",
    )

    @property
    def database_url(self) -> URL:

        return URL.create(
            drivername    = "postgresql+asyncpg",
            username      = self.DB_USER,
            password      = self.DB_PASSWORD.get_secret_value(),
            host          = self.DB_HOST,
            port          = self.DB_PORT,
            database      = self.DB_NAME,
        )



@lru_cache
def get_settings() -> Settings:
    return Settings()


settings = get_settings()
