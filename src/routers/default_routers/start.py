import logging
from pathlib import Path

from aiogram import Router
from aiogram.filters import CommandStart
from aiogram.types import Message, FSInputFile
from aiogram.utils.markdown import hbold

router: Router = Router(name=__name__)
logger = logging.getLogger(__name__)


@router.message(CommandStart())
async def start_handler(message: Message) -> None:
    logger.info("Пользователь выбрал команду 'start'")
    file_path: Path = Path(__file__).parent.parent.parent.joinpath(
        "media", "magnit_1.jpg"
    )
    await message.reply_photo(
        photo=FSInputFile(path=file_path),
        caption=hbold("Привет я бот по доставке цветов"),
    )
