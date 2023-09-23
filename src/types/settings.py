from pydantic import SecretStr, PostgresDsn, RedisDsn

DATABASE_URL = 'postgresql://bot:qwerty@postgres-fb-bot:5432/bot2'  # docker db
# DATABASE_URL = 'postgresql://bot:qwerty@127.0.0.1:5432/bot'  # local db

# TOKEN = '6306652:AAE_CO07WXocfidvniOKJ4HloTzjaYA0QzU'  # main TOKEN
TOKEN = '6366199783:AAF0vbIzEo3g4hO7riXs-q0dFZEOdb6_sBM'  # test TOKEn
# TOKEN = '5888133619:AAE1XW55jVt-pqpkXma1PcmoNGFK8m0v9eE'  # test TOKEn weather


class Settings:
    BOT_TOKEN: SecretStr
    # DATABASE_URL = 'postgresql://bot:qwerty@postgres:5432/bot'
    DATABASE_ASYNC_URL: PostgresDsn
    CELERY_BROKER_URL: RedisDsn
    CELERY_RESULT_BACKEND: RedisDsn


class NoLinksException(BaseException):
    pass


class UserConnectionError(BaseException):
    pass


class NoDataFromUrl(BaseException):
    pass


class NoUrlsFromParse(BaseException):
    pass
