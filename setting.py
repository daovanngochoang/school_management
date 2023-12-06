import secrets
from typing import Optional, Dict, Any

from dotenv import load_dotenv
from pydantic import (
    PostgresDsn, field_validator,
)

from pydantic_settings import BaseSettings

load_dotenv(".env")


class Settings(BaseSettings):
    SERVER_HOST: str = "localhost"
    SERVER_PORT: str = "8080"
    SECRET_KEY: str = secrets.token_urlsafe(32)

    # 60 minutes * 24 hours * 8 days = 8 days
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 8

    POSTGRES_SERVER: str
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_DB: str
    POSTGRES_PORT: str

    SQLALCHEMY_DATABASE_URI: Optional[PostgresDsn] = None

    @field_validator("SQLALCHEMY_DATABASE_URI", mode="after")
    @classmethod
    def assemble_db_connection(cls, v: Optional[str], values) -> Any:
        if isinstance(v, str):
            return v
        print(values.data)
        return PostgresDsn.build(
            scheme="postgresql+psycopg",
            username=values.data.get("POSTGRES_USER"),
            password=values.data.get("POSTGRES_PASSWORD"),
            host=values.data.get("POSTGRES_SERVER"),
            port=int(values.data.get("POSTGRES_PORT")),
            path=f"{values.data.get('POSTGRES_DB')}",
        )


settings = Settings()
