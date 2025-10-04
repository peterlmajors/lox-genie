from pydantic_settings import BaseSettings

class Settings(BaseSettings):

    NAME: str = "Lox API"
    DESCRIPTION: str = "Application Programming Interface for Lox Genie"
    VERSION: str = "1.0.0"
    ENV: str = 'dev'

    DEBUG: bool = True
    LOG_LEVEL: str = "INFO"
    HOST: str = "0.0.0.0"
    PORT: int = 8000

settings = Settings()