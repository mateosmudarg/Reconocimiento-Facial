from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Configuración central cargada desde variables de entorno / .env."""

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    database_url: str = "postgresql+asyncpg://recfac:recfac@localhost:5432/recfac"

    secret_key: str = "dev-insecure-change-me"
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 480

    face_match_threshold: float = 0.45

    admin_username: str = "admin"
    admin_password: str = "admin123"


@lru_cache
def get_settings() -> Settings:
    return Settings()


settings = get_settings()
