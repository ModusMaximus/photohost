from aiogram.fsm.state import State, StatesGroup


class Photo(StatesGroup):
    Count = State()
    photo_id = State()
