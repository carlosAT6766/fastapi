"""Application settings loaded from environment variables."""

from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    # Database
    database_url: str = "postgresql+asyncpg://resumeai:resumeai@postgres:5432/resumeai"

    # Redis (queue + pub/sub)
    redis_host: str = "redis"
    redis_port: int = 6379
    redis_db: int = 0

    # Auth
    jwt_secret: str = "change-me-in-prod"
    jwt_algorithm: str = "HS256"
    access_token_expire_minutes: int = 60

    # OpenAI (falls back to fake summarizer when empty)
    openai_api_key: str = ""
    openai_model: str = "gpt-4o-mini"

    # Seeded demo/customer accounts
    demo_admin_username: str = "admin"
    demo_admin_password: str = "admin123"
    storefront_customer_email: str = "customer@resumeai.com"


@lru_cache
def get_settings() -> Settings:
    return Settings()
