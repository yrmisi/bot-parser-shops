from time import sleep
from typing import Union

from aiogram.types import Message, CallbackQuery


async def del_msg(msg: Union[Message | CallbackQuery], sec: int = None) -> None:
    if sec is None:
        sec = 1
    sleep(sec)
    await msg.delete()
