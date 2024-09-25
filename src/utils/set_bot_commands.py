from aiogram.types import BotCommand

from src.config_data.config import DEFAULT_COMMANDS


async def set_default_commands(bot) -> None:
    await bot.set_my_commands(
        [
            BotCommand(command=command[0], description=command[1])
            for command in DEFAULT_COMMANDS
        ]
    )
