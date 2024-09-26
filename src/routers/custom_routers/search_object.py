import logging
from pathlib import Path
from typing import Dict

from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery, FSInputFile
from aiogram.filters import Command
from aiogram import F, Router
from fake_useragent import UserAgent

from keyboards.inline.lot_buttons_and_stops import buttons_and_stop
from parsing_catalog_product.start_store_search import get_store
from utils.my_callback import MyCallback
from utils.state import StateProductSearch
from utils.delet_message import del_msg

router = Router(name=__name__)
logger = logging.getLogger(__name__)


@router.message(Command("search"))
async def handler_search(message: Message, state: FSMContext) -> None:
    logger.info("Функция 'handler_search' пользователь ввел команду 'search'")
    file_path: Path = Path(__file__).parent.parent.parent.joinpath(
        "media", "product_1.jpg"
    )
    await message.reply_photo(
        photo=FSInputFile(path=file_path),
        caption="Выбери продуктовый маркетплейс",
        reply_markup=buttons_and_stop(
            ["search|magnit|Магнит", "search|pyaterochka|Пятерочка"], "search|stop|СТОП"
        ),
    )
    await state.set_state(StateProductSearch.shops)


@router.callback_query(MyCallback.filter(F.command == "search"))
async def my_callback_foo(
    call: CallbackQuery, callback_data: MyCallback, state: FSMContext
) -> None:
    logger.info(
        f"Функция my_callback_foo пользователь нажал кнопку {callback_data.name_button}"
    )

    if callback_data.item == "stop":
        file_path: Path = Path(__file__).parent.parent.parent.joinpath(
            "media", "see_you_again_1.jpg"
        )
        await call.message.reply_photo(
            photo=FSInputFile(path=file_path), caption="Пока"
        )
        await state.clear()

    else:
        await state.update_data(
            shop=callback_data.item, button=callback_data.name_button
        )
        await choice_shops(call.message, state)

    await del_msg(call.message, 3)


@router.message(StateProductSearch.shops)
async def choice_shops(message: Message, state: FSMContext) -> None:
    logger.info("Функция 'choice_shops' пользователь выбирает магазин")
    data: Dict[str, str] = await state.get_data()

    if message.from_user.is_bot and data["shop"] == "magnit":
        await message.answer(text=f"Загружаем розничную сеть Магнит. \nПодожди немного")

        user_agent: UserAgent = UserAgent(os=["windows"]).random
        url: str = r"https://magnit.ru/"
        await state.update_data(user_agent=user_agent, url=url)
        await state.set_state(StateProductSearch.open_site)
        await get_store(message, state)

    elif message.from_user.is_bot and data["shop"] == "pyaterochka":
        await message.answer(text=f"Сайт находиться в разработке")
        await state.clear()

    else:
        msg: Message = await message.answer(text="Нажми на кнопку")
        await del_msg(message)
        await del_msg(msg, 3)
