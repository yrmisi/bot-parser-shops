import logging

from aiogram import F, Router
from aiogram.types import Message

router = Router(name=__name__)
logger = logging.getLogger(__name__)


@router.message(F.text.regexp(r"[привет, ПРИВЕТ, ghbd, GHBD]{4,}"))
async def handler_hello(message: Message) -> None:
    logger.info("Функция 'handler_hello' пользователь ввел слово 'привет'")
    await message.reply(text="И тебе привет")
