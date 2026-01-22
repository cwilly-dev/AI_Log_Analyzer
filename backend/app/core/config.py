import secrets
from typing import Annotated, Any
from pydantic import AnyUrl, BeforeValidator, computed_field
from pydantic_settings import BaseSettings, SettingsConfigDict

def parse_origins(v: Any) -> list[str] | str:
    if isinstance(v, str) and not v.startswith("["):
        return [i.strip() for i in v.split(",") if i.strip()]
    elif isinstance(v, (list, str)):
        return v
    raise ValueError(v)

class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=True,
        env_ignore_empty=False,
        extra="ignore",
    )
    PROJECT_NAME: str
    PROJECT_VERSION: str

    API_PREFIX: str = "/api"
    DATABASE_URL: str

    ALGORITHM: str
    SECRET_KEY: str

    DEBUG: bool = False

    OPENAI_API_KEY: str
    OPENAI_MODEL:  str

    GEMINI_API_KEY: str
    GEMINI_MODEL: str

    GROK_API_KEY: str
    GROK_MODEL: str

    CORS_ORIGINS: Annotated[
        list[AnyUrl] | str, BeforeValidator(parse_origins)
    ] = []

    FRONTEND_HOST: str

    TOKEN_EXPIRE_MINS: int = 60 * 24 * 8

    @computed_field
    @property
    def all_origins(self) -> list[str]:
        return[str(origin).rstrip("/") for origin in self.CORS_ORIGINS] + [
            self.FRONTEND_HOST
        ]

settings = Settings()