from aiogram import Router, types, Bot
from aiogram.filters import CommandStart

from keyboards.kb_admin import kb_main_admin
from filters.my_filter import AdmFilter
from parser1 import img_by_id, all_pars
from data import orm


router: Router = Router()
router.message.filter(AdmFilter())  # применяем ко всем хендлерам фильтр на админа


@router.message(CommandStart())
async def start_admin(msg: types.Message):
    await msg.answer(text='Привет', reply_markup=kb_main_admin)





# @router.message()
# async def eho_admin(msg: types.Message):
#     await msg.answer(text='ответcvbcv', reply_markup=kb_main_admin)

# @router.callback_query()
