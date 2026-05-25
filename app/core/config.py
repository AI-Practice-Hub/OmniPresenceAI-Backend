from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    MONGODB_URL: str = ""
    DATABASE_NAME: str = ""
    SECRET_KEY: str = ""
    ALGORITHM: str = ""
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 1440
    AZURE_STORAGE_CONNECTION_STRING: str = ""
    AZURE_CONTAINER_NAME: str = ""

    # Azure OpenAI Variables
    AZURE_OPENAI_API_KEY: str = ""
    AZURE_OPENAI_ENDPOINT: str = ""
    AZURE_OPENAI_API_VERSION: str = "2024-02-01"
    AZURE_OPENAI_DEPLOYMENT_NAME: str = ""

    class Config:
        env_file = ".env"

settings = Settings()