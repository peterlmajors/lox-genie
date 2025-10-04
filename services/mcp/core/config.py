from pydantic_settings import BaseSettings

class Settings(BaseSettings):

    NAME: str = "Lox MCP"
    DESCRIPTION: str = "Model Context Protocol Server for Lox Genie"
    VERSION: str = "1.0.0"
    ENV: str = 'dev'

    DEBUG: bool = True
    LOG_LEVEL: str = "INFO"
    HOST: str = "0.0.0.0"
    PORT: int = 8001

    SLEEPER_API_URL: str = "https://api.sleeper.app/v1"
    NFL_YEAR: int = 2025

settings = Settings()