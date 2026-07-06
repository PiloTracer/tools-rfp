"""Application configuration."""

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    database_url: str = "postgresql+asyncpg://rfp:rfp@localhost:5432/rfp"
    redis_url: str = "redis://localhost:6379/0"
    minio_endpoint: str = "localhost:9000"
    minio_access_key: str = "rfp_access"
    minio_secret_key: str = ""
    jwt_secret: str = ""
    litellm_api_key: str = ""
    litellm_provider: str = "openai"
    litellm_model: str = "gpt-4o"
    rfp_max_upload_mb: int = 50
    rate_limit_per_min: int = 100

    class Config:
        env_file = ".env"


settings = Settings()
