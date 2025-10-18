from pydantic_settings import BaseSettings

class Settings(BaseSettings):

    # Application
    NAME: str = "Lox API"
    VERSION: str = "1.0.0"
    ENV: str = 'local'

    # Logging
    DEBUG: bool = True
    LOG_LEVEL: str = "INFO"

    # Server
    HOST: str = "0.0.0.0"
    PORT: int = 8000

    # LLM
    LLM_BASE_URL: str = "http://llama:8002"

    # MongoDB
    MONGODB_HOST: str = "mongodb"
    MONGODB_PORT: int = 27017
    MONGODB_USERNAME: str = "admin"
    MONGODB_PASSWORD: str = "password"
    MONGODB_DATABASE: str = "lox-genie"

    # Sleeper API
    SLEEPER_API_URL: str = "https://api.sleeper.app/v1"
    
    class Config:
        env_file = ".env"
        case_sensitive = True

settings = Settings()