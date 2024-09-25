import logging

from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message
from aiogram.utils.markdown import hbold

from src.config_data.config import DEFAULT_COMMANDS

router = Router(name=__name__)
logger = logging.getLogger(__name__)


@router.message(Command("help", prefix="/!"))
async def help_handler(message: Message) -> None:
    logger.info("Функция 'help_handler' запущен")
    text = [
        f"/{hbold(command)} - {hbold(description)}"
        for command, description in DEFAULT_COMMANDS
    ]
    await message.answer(text="\n".join(text))
