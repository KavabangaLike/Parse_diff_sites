from pydantic import BaseSettings, SecretStr, PostgresDsn, RedisDsn


class Settings(BaseSettings):
    BOT_TOKEN: SecretStr
    DATABASE_URL: PostgresDsn
    DATABASE_ASYNC_URL: PostgresDsn
    CELERY_BROKER_URL: RedisDsn
    CELERY_RESULT_BACKEND: RedisDsn
