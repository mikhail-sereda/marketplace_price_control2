from aiogram.fsm.state import StatesGroup, State


class FiltersFSM(StatesGroup):
    name_tariff = State()
    tracked_items = State()
    price_tariff = State()


class AddMoneyFSM(StatesGroup):
    amount_money = State()


class AddAdvertisementFSM(StatesGroup):
    img = State()
    text = State()
    button_link = State()
