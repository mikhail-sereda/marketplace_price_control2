from aiogram import Router, types
from aiogram.filters import CommandStart

from keyboards.kb_user import kb_main_user
from data import orm

router: Router = Router()


@router.message(CommandStart())
async def start_other(msg: types.Message):
    """при входе нового пользователя добавляет в БД"""
    orm.add_user(msg.from_user.id)
    await msg.answer(text=f'Привет {msg.from_user.first_name}', reply_markup=kb_main_user)