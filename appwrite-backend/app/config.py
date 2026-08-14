from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    APPWRITE_ENDPOINT: str
    APPWRITE_PROJECT_ID: str
    APPWRITE_API_KEY: str

    DATABASE_ID: str
    USERS_COLLECTION_ID: str
    FILES_COLLECTION_ID: str

    BUCKET_ID: str

    class Config:
        env_file = ".env"


settings = Settings()