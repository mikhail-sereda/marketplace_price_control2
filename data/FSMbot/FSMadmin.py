from aiogram.fsm.state import StatesGroup, State


class FiltersFSM(StatesGroup):
    name_tariff = State()
    tracked_items = State()
    price_tariff = State()