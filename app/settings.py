from functools import cache

import pydantic
from pydantic.networks import RedisDsn
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=True,
        extra="ignore",
    )


class DBSettings(Settings):
    POSTGRES_HOST: str = "127.0.0.1"
    POSTGRES_USER: str = "app_user"
    POSTGRES_PASSWORD: str = "password"
    POSTGRES_PORT: int = 5432
    POSTGRES_DB: str = "app_db"

    @property
    def uri(self) -> str:
        dsn = pydantic.PostgresDsn.build(
            scheme="postgresql",
            username=self.POSTGRES_USER,
            password=self.POSTGRES_PASSWORD,
            host=self.POSTGRES_HOST,
            port=self.POSTGRES_PORT,
            path=self.POSTGRES_DB,
        )
        return str(dsn)


class CoreSettings(Settings):
    DEBUG: bool = False
    ENVIRONMENT: str = "local"


class SentrySettings(Settings):
    model_config = SettingsConfigDict(env_prefix="SENTRY_")

    DSN: str = ""
    SAMPLE_RATE: float = 0.1
    PROFILES_SAMPLE_RATE: float = 1.0


class RedisSettings(BaseSettings):
    model_config = SettingsConfigDict(env_prefix="REDIS_")

    HOST: str = "127.0.0.1"
    PORT: int = 6379
    DB: int = 2  # Currently 0 and 1 are occupied by other services
    PASSWORD: str | None = None

    @property
    def dsn(self) -> str:
        dsn = RedisDsn.build(
            scheme="redis",
            host=self.HOST,
            port=self.PORT,
            path=str(self.DB),
            password=self.PASSWORD,
        )
        return str(dsn)


class AppSettings:
    core = CoreSettings()
    db = DBSettings()
    sentry = SentrySettings()
    redis = RedisSettings()


@cache
def get_app_settings() -> AppSettings:
    return AppSettings()
