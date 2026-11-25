from pydantic_settings import BaseSettings
from typing import List
import os


class Settings(BaseSettings):
    DATABASE_URL: str = "sqlite:///./lotus_studio.db"
    SECRET_KEY: str = "lotus-studio-super-secret-key-change-in-production"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 15
    REFRESH_TOKEN_EXPIRE_DAYS: int = 7
    SALT_ROUNDS: int = 12
    CORS_ORIGINS: str = "http://localhost:3000"
    ENVIRONMENT: str = "development"
    DEBUG: bool = True
    APP_NAME: str = "Lotus Studio"
    APP_VERSION: str = "1.0.0"
    ADMIN_EMAIL: str = "admin@lotusstudio.dev"
    TOTP_ISSUER: str = "LotusStudio"
    CSRF_SECRET: str = "lotus-csrf-secret-key-change-in-production"
    RATE_LIMIT_PER_MINUTE: int = 60

    @property
    def cors_origins_list(self) -> List[str]:
        return [o.strip() for o in self.CORS_ORIGINS.split(",")]

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


settings = Settings()
