import os
from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field

class Settings(BaseSettings):
    huntapi_api_key: str = Field(default="test_key", validation_alias="HUNTAPI_API_KEY")
    huntapi_base_url: str = Field(default="https://api.huntapi.com/v1/video/download", validation_alias="HUNTAPI_BASE_URL")
    downloads_dir: str = Field(default="./downloads", validation_alias="DOWNLOADS_DIR")

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")

settings = Settings()
