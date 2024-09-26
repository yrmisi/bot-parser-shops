import logging
from datetime import datetime, timedelta
from pathlib import Path

from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message, FSInputFile

router: Router = Router(name=__name__)
logger = logging.getLogger(__name__)


@router.message(Command("new_year"))
async def handler_new_year(message: Message) -> None:
    logger.info("Функция handler_new_year пользователь ввел команду 'new_year'")
    # определяем разницу до нового года
    next_year: int = datetime.now().year + 1
    new_year: str = f"{next_year}-01-01 00:00:00"
    current_date: datetime = datetime.now().replace(microsecond=0)
    format_new_year: datetime = datetime.strptime(new_year, "%Y-%m-%d %H:%M:%S")
    t_delta: timedelta = format_new_year - current_date

    text: str = f"До Нового Года осталось {str(t_delta).replace("days,", "дня")}"
    file_path: Path = Path(__file__).parent.parent.parent.joinpath(
        "media", "new_year_1.jpg"
    )
    await message.reply_photo(photo=FSInputFile(path=file_path), caption=text)
