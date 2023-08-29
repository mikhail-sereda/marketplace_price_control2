from aiogram.filters import Filter
from aiogram.types import Message

from data import orm


class AdmFilter(Filter):
    async def __call__(self, msg: Message):
        return str(msg.from_user.id) == orm.ADMIN_ID


class UserFilt(Filter):
    async def __call__(self, msg: Message):
        print(22)
        return not orm.db_my_filter_user(msg.from_user.id)
