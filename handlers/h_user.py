from aiogram import Router, types
from aiogram.filters import CommandStart


router: Router = Router()


@router.message(CommandStart())
async def start_user(msg: types.Message):
    await msg.answer(text='привет user]')


@router.message()
async def eho_admin(msg: types.Message):
    await msg.answer(text='ответ')

