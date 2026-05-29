from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    server_url: str = "http://localhost:8000"
    device_name: str = "Kiosko"
    camera_index: int = 0

    face_model: str = "buffalo_l"
    face_provider: str = "CPUExecutionProvider"

    arduino_port: str = ""
    arduino_baud: int = 9600


@lru_cache
def get_settings() -> Settings:
    return Settings()


settings = get_settings()
