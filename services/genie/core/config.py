from pydantic_settings import BaseSettings
from typing import Optional


class Settings(BaseSettings):

    NAME: str = "Lox API"
    DESCRIPTION: str = "Fantasy Football API with MCP Server"
    VERSION: str = "1.0.0"
    ENV: str

    DEBUG: bool = True
    LOG_LEVEL: str = "INFO"
    HOST: str = "0.0.0.0"
    PORT: int = 8000

    NFL_YEAR: int = 2025
    SLEEPER_API_URL: str = "https://api.sleeper.app/v1"

    GEMINI_API_KEY: Optional[str]
    AWS_IAM_ACCOUNT_ID: Optional[str]
    AWS_ACCESS_KEY_ID: Optional[str]
    AWS_SECRET_ACCESS_KEY: Optional[str]
    ODDS_API_KEY: Optional[str]
    CFBD_API_KEY: Optional[str]

    class Config:
        env_file = ".env"
        case_sensitive = True

settings = Settings()