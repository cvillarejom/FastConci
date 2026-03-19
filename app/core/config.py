from pydantic_settings import BaseSettings, SettingsConfigDict
from functools import lru_cache

from typing import List

class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file= "./.env",
        env_ignore_empty=True,
        extra="ignore"
    )

    env: str
    app_name: str = "Fast-Api"
    debug: bool
    version: str

    database_port: str
    database_url: str
    database_user: str
    database_password: str
    database_name: str

    secret_key: str
    algorithm:str
    access_token_expire_in_minutes: int


    allowed_origins: List[str]



@lru_cache
def get_settings():
    return Settings()