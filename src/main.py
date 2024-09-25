import asyncio
import logging
import sys

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.fsm.storage.memory import MemoryStorage

from config_data.config import bot_setting
from parsing_catalog_product import router as parser_router
from routers import router as main_router
from utils.set_bot_commands import set_default_commands

logger = logging.getLogger(__name__)


async def main() -> None:
    logger.info("Run bot")
    bot: Bot = Bot(
        token=bot_setting.token.get_secret_value(),
        default=DefaultBotProperties(parse_mode="HTML"),
    )
    storage: MemoryStorage = MemoryStorage()
    dp: Dispatcher = Dispatcher(storage=storage)
    dp.include_routers(parser_router, main_router)

    await set_default_commands(bot)
    await bot.delete_webhook(
        drop_pending_updates=True
    )  # удаляет все обновления, которые произошли после последнего завершения работы бота
    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(
        format="%(levelname)s | %(name)s | %(asctime)s.%(msecs)3d | %(lineno)d | %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
        level=20,
        stream=sys.stdout,
    )
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.error("Stop bot")
