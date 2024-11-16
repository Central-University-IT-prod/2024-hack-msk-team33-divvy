from aiogram.dispatcher.filters.state import State, StatesGroup


class MainStates(StatesGroup):
    wait_number = State()
    is_card = State()
    wait_card = State()
    all_done = State()
