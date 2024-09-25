from aiogram.fsm.state import StatesGroup, State


class StateProductSearch(StatesGroup):
    shops: State = State()
    open_site: State = State()
    city_input: State = State()
    store_selection: State = State()
    categories: State = State()
    category_number: State = State()
    product: State = State()
    parser: State = State()
