import logging

from aiogram import Router
from aiogram.types import Message

router = Router(name=__name__)
logger = logging.getLogger(__name__)


@router.message()
async def echo_handler(message: Message) -> None:
    logger.info("Функция 'echo_handler'")
    await message.answer(text="Подожди секунду...", parse_mode=None)
    try:
        await message.copy_to(chat_id=message.chat.id)
    except TypeError:
        await message.reply("Эхо без состояния или фильтров. \nИ что ты мне отправил")
