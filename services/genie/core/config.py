from pydantic_settings import BaseSettings
from typing import Optional


class Settings(BaseSettings):

    NAME: str = "Lox API"
    DESCRIPTION: str = "Fantasy Football API with MCP Server"
    VERSION: str = "1.0.0"
    ENV: str = "dev"

    DEBUG: bool = True
    LOG_LEVEL: str = "INFO"

    # Server configuration
    HOST: str = "0.0.0.0"
    PORT: int = 8000

    NFL_YEAR: int = 2025
    SLEEPER_API_URL: str = "https://api.sleeper.app/v1"

    # AWS settings (optional for development)
    AWS_IAM_ACCOUNT_ID: Optional[str] = None
    AWS_ACCESS_KEY_ID: Optional[str] = None
    AWS_SECRET_ACCESS_KEY: Optional[str] = None

    class Config:
        env_file = ".env"
        case_sensitive = True


settings = Settings()
