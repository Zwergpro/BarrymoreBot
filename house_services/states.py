from aiogram.dispatcher.filters.state import StatesGroup, State


class UserInformation(StatesGroup):
    fio = State()
    address = State()
    confirmation = State()
