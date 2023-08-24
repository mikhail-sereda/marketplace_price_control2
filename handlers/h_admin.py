from aiogram import Router, types
from aiogram.filters import CommandStart

from keyboards.kb_admin import kb_main_admin
from filters.filters import AdmFilter

router: Router = Router()
router.message.filter(AdmFilter())


@router.message(CommandStart())
async def start_admin(msg: types.Message):
    await msg.answer(text='Привет')


@router.message()
async def eho_admin(msg: types.Message):
    await msg.answer(text='ответ', reply_markup=kb_main_admin)


@router.message()
async def eho_user(msg: types.Message):
    await msg.answer(text='ты не админ')


#@router.callback_query()
