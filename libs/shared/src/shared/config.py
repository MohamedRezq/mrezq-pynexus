from pydantic import PostgresDsn, RedisDsn, SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",  # ignore unknown env vars — safe default
    )

    # Application
    app_name: str = "PyNexus"
    debug: bool = False
    environment: str = "development"

    # Database
    database_url: PostgresDsn
    db_pool_size: int = 10
    db_max_overflow: int = 20

    # Redis
    redis_url: RedisDsn = "redis://localhost:6379/0"  # type: ignore[assignment]

    # Security — SecretStr prevents secret leaking in logs/tracebacks
    secret_key: SecretStr
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 30
    refresh_token_expire_days: int = 7

    # Storage
    s3_bucket: str = "pynexus-docs"
    s3_region: str = "eu-central-1"
    aws_access_key_id: SecretStr | None = None
    aws_secret_access_key: SecretStr | None = None

    # External APIs
    openai_api_key: SecretStr | None = None

    # Observability
    sentry_dsn: str | None = None


# Import this singleton everywhere — never instantiate Settings() again
settings = Settings()  # type: ignore[call-arg]
