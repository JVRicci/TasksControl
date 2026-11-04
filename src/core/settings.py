from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """API Settings schema"""

    APP_NAME: str
    ENV: str

    DATABASE_URL: str

    # SECRET_KEY: str
    # JWT_ALGORITHM: str
    # JWT_ACCESS_TOKEN_EXPIRES_TIME: int

    class Config:
        """Setting configuration"""

        env_file = ".env"
        env_file_encoding = "utf-8"


settings = Settings()
