from pydantic_settings import BaseSettings, SettingsConfigDict
from functools import lru_cache

class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file= "./.env",
        env_ignore_empty=True,
        extra="ignore"
    )

    app_name: str = "Fast-Api"



@lru_cache
def get_settings():
    return Settings()