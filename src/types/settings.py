from pydantic import SecretStr, PostgresDsn, RedisDsn

DATABASE_URL = 'postgresql://bot:qwerty@postgres-fb-bot:5432/bot'


class Settings:
    BOT_TOKEN: SecretStr
    # DATABASE_URL = 'postgresql://bot:qwerty@postgres:5432/bot'
    DATABASE_ASYNC_URL: PostgresDsn
    CELERY_BROKER_URL: RedisDsn
    CELERY_RESULT_BACKEND: RedisDsn


NoLinksException, UserConnectionError, NoDataFromUrl, NoUrlsFromParse = BaseException(), BaseException(), \
    BaseException(), BaseException()
