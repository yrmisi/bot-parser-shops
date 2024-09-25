from aiogram.utils.keyboard import (
    InlineKeyboardBuilder,
    InlineKeyboardMarkup,
)

from src.utils.my_callback import MyCallback


def buttons_and_stop(data, stop) -> InlineKeyboardMarkup:
    keyboard: InlineKeyboardBuilder = InlineKeyboardBuilder()

    for elem in data:
        keyboard.button(
            text=elem.split("|")[-1],
            callback_data=MyCallback(
                command=elem.split("|")[0],
                item=elem.split("|")[1],
                name_button=elem.split("|")[-1],
            ),
        )

    keyboard.button(
        text=stop.split("|")[-1],
        callback_data=MyCallback(
            command=stop.split("|")[0],
            item=stop.split("|")[1],
            name_button=stop.split("|")[-1],
        ),
    )

    keyboard.adjust(2, 1)

    return keyboard.as_markup()

    # keyboard_lst = []
    #
    # for elem in data:
    #     keyboard_lst.append(
    #         InlineKeyboardButton(text=elem.split("|")[1], callback_data=elem)
    #     )
    # button_stop = InlineKeyboardButton(text=stop.split("|")[1], callback_data=stop)
    # keyboard = InlineKeyboardMarkup(inline_keyboard=[keyboard_lst, [button_stop]])
    #
    # return keyboard
