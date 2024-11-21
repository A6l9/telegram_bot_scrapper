from aiogram.fsm.state import State, StatesGroup


class States(StatesGroup):
    write_keyword = State()
    write_subs_count = State()
