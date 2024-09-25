from aiogram.filters.callback_data import CallbackData


class MyCallback(CallbackData, prefix="my"):
    command: str
    item: str
    name_button: str


if __name__ == "__main__":
    MyCallback()
