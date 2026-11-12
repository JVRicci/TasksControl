from pydantic import ConfigDict
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """API Settings schema"""

    APP_NAME: str
    ENV: str

    DATABASE_URL: str

    TEST_DATABASE_URL: str

    JWT_SECRET_KEY: str
    JWT_ACCESS_TOKEN_EXPIRES_MINUTES: int = 15

    model_config = ConfigDict(env_file=".env", env_file_encoding="utf-8")


settings = Settings()
