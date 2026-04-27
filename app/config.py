"""
Application configuration with environment-based settings
"""

import os
from typing import List, Optional
from enum import Enum
from pydantic_settings import BaseSettings


class Environment(str, Enum):
    """Application environment"""
    DEVELOPMENT = "development"
    STAGING = "staging"
    PRODUCTION = "production"


class Settings(BaseSettings):
    """Application settings loaded from environment variables"""

    # Application
    APP_NAME: str = "EduPal API"
    APP_VERSION: str = "1.0.0"
    ENVIRONMENT: Environment = Environment.DEVELOPMENT
    DEBUG: bool = False

    # Server
    HOST: str = "0.0.0.0"
    PORT: int = 8000
    WORKERS: int = 4

    # Database
    DATABASE_URL: str = "sqlite:///./edupal.db"
    DATABASE_ECHO: bool = False
    DATABASE_POOL_SIZE: int = 20
    DATABASE_POOL_RECYCLE: int = 3600
    DATABASE_POOL_PRE_PING: bool = True

    # CORS
    CORS_ORIGINS: List[str] = ["*"]
    CORS_CREDENTIALS: bool = True
    CORS_METHODS: List[str] = ["*"]
    CORS_HEADERS: List[str] = ["*"]

    # Logging
    LOG_LEVEL: str = "INFO"
    LOG_FORMAT: str = "json"  # "json" or "text"

    # API
    API_V1_PREFIX: str = "/api/v1"
    API_TITLE: str = "EduPal API"
    API_DESCRIPTION: str = "Offline Learning Assistant Platform API"

    # Security
    ALLOW_ORIGINS_REGEX: Optional[str] = None
    ALLOWED_HOSTS: List[str] = ["*"]

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = True

    @property
    def is_production(self) -> bool:
        """Check if running in production"""
        return self.ENVIRONMENT == Environment.PRODUCTION

    @property
    def is_development(self) -> bool:
        """Check if running in development"""
        return self.ENVIRONMENT == Environment.DEVELOPMENT

    @property
    def database_config(self) -> dict:
        """Get database configuration"""
        config = {
            "url": self.DATABASE_URL,
            "echo": self.DATABASE_ECHO,
        }
        if "postgresql" in self.DATABASE_URL or "mysql" in self.DATABASE_URL:
            config.update({
                "pool_size": self.DATABASE_POOL_SIZE,
                "max_overflow": 10,
                "pool_recycle": self.DATABASE_POOL_RECYCLE,
                "pool_pre_ping": self.DATABASE_POOL_PRE_PING,
            })
        return config


# Load settings
settings = Settings()
