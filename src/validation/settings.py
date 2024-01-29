from pydantic import SecretStr, PostgresDsn
from pydantic_settings import BaseSettings
# DATABASE_URL = 'postgresql://bot:qwerty@postgres-fb-bot:5432/bot2'  # docker db
# DATABASE_URL = 'postgresql://bot:qwerty@127.0.0.1:5432/bot'  # local db

# TOKEN = '6306652:AAE_CO07WXocfidvniOKJ4HloTzjaYA0QzU'  # main TOKEN
# TOKEN = '6366199783:AAF0vbIzEo3g4hO7riXs-q0dFZEOdb6_sBM'  # test TOKEn
# TOKEN = '5888133619:AAE1XW55jVt-pqpkXma1PcmoNGFK8m0v9eE'  # test TOKEn weather
# TOKEN = '6249543267:AAEOPQvoj6Zo6-ufviJjZ6yTZ8Z6OPkqoXY'  # new?


class Settings(BaseSettings):
    # BOT_TOKEN: SecretStr  = '6366199783:AAF0vbIzEo3g4hO7riXs-q0dFZEOdb6_sBM'  # test TOKEn
    BOT_TOKEN: SecretStr = '5888133619:AAE1XW55jVt-pqpkXma1PcmoNGFK8m0v9eE'  # test TOKEn
    # DATABASE_URL: PostgresDsn  # = 'postgresql://bot:qwerty@postgres-fb-bot:5432/bot2'  # docker db
    DATABASE_URL: PostgresDsn = "postgresql://bot:qwerty@localhost:5432/bot3"  # docker db


settings = Settings()


class NoLinksException(BaseException):
    pass


class UserConnectionError(BaseException):
    pass


class NoDataFromUrl(BaseException):
    pass


class NoUrlsFromParse(BaseException):
    pass
