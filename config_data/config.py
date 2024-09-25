from dotenv import load_dotenv, find_dotenv
from os import getenv

from pydantic_settings import BaseSettings
from pydantic import SecretStr


if not find_dotenv():
    exit("Переменное окружение не загружено, т.к. отсутствует файл .env")
else:
    load_dotenv()

BOT_TOKEN = getenv("BOT_TOKEN")
if BOT_TOKEN is None:
    exit("BOT_TOKEN отсутствует в переменном окружении")

DEFAULT_COMMANDS = (
    ("start", "Запустить бота"),
    ("help", "Вывести справку"),
    ("search", "Поищем, что нибудь"),
    ("new_year", "До Нового года осталось"),
)


class BotSecretStr(BaseSettings):
    token: SecretStr = getenv("BOT_TOKEN")


bot_setting = BotSecretStr()
