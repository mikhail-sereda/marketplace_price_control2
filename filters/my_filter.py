import re

from aiogram.filters import Filter
from aiogram.types import Message

from data import orm


class AdmFilter(Filter):
    async def __call__(self, msg: Message):
        return str(msg.from_user.id) == orm.ADMIN_ID


class UserFilt(Filter):
    async def __call__(self, msg: Message):
        return not orm.db_my_filter_user(msg.from_user.id)


class CheckTariff(Filter):
    async def __call__(self, msg: Message):
        user = orm.db_get_profile(msg.from_user.id)
        count_product = orm.db_get_count_product_user(msg.from_user.id)

        if count_product >= user.tracked_items:
            await msg.answer(f'У вас действует тариф:\n{user.tariff_user}.\n'
                             f'Максимально можно добавить до {user.tracked_items} ссылок')
            return False
        elif count_product < user.tracked_items:
            return True


class CheckLink(Filter):
    async def __call__(self, msg: Message):
        a = re.compile(r'\Swildberries.ru/catalog/\d+/\S')
        print(bool(a.findall(msg.text)))
        return bool(a.findall(msg.text))
