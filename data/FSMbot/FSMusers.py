from aiogram.fsm.state import StatesGroup, State


class ChequeFSM(StatesGroup):
    screen_cheque = State()
