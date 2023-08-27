from aiogram import Router, types
from aiogram.filters import CommandStart

from keyboards.kb_admin import kb_main_admin
from filters.my_filter import AdmFilter
from parser import img_by_id, all_pars

router: Router = Router()
router.message.filter(AdmFilter())  # применяем ко всем хендлерам фильтр на админа


@router.message(CommandStart())
async def start_admin(msg: types.Message):
    await msg.answer(text='Привет', reply_markup=kb_main_admin)


@router.message()
async def parsing_link(msg: types.Message):
    url_list = msg.text.split('/')
    id_prod = filter(lambda x: x.isnumeric(), url_list)
    try:
        id_prod = list(id_prod)[0]
    except IndexError:
        await msg.answer(text='Не верная ссылка', reply_markup=kb_main_admin)
    img_link = img_by_id(id_prod)
    prod_info = all_pars(id_prod)
    print(msg.text)
    print(id_prod)
    print(img_link)
    print(prod_info)


@router.message()
async def eho_admin(msg: types.Message):
    await msg.answer(text='ответcvbcv', reply_markup=kb_main_admin)

# @router.callback_query()
