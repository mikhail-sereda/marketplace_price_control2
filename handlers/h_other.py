from aiogram import Router, types
from aiogram.filters import CommandStart

from keyboards.kb_user import kb_main_user


router: Router = Router()


@router.message(CommandStart())
async def start_other(msg: types.Message):
    """при входе нового пользователя добавляет в БД"""
    await msg.answer(text=f'Привет {msg.from_user.first_name}', reply_markup=kb_main_user)