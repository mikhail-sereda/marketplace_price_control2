from aiogram.filters import Filter
from aiogram.types import Message
from main import ADMIN_ID


class AdmFilter(Filter):
    async def __call__(self, msg: Message):
        return str(msg.from_user.id) == ADMIN_ID


