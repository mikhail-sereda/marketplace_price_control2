from aiogram import Router, types, Bot
from aiogram.filters import CommandStart

from keyboards.kb_admin import kb_main_admin
from filters.my_filter import AdmFilter
from parser import img_by_id, all_pars
from data import orm


router: Router = Router()
router.message.filter(AdmFilter())  # применяем ко всем хендлерам фильтр на админа


@router.message(CommandStart())
async def start_admin(msg: types.Message):
    await msg.answer(text='Привет', reply_markup=kb_main_admin)


@router.message()
async def parsing_link(msg: types.Message):
    product_dict = {'user_id': msg.from_user.id, 'link': msg.text}
    url_list = msg.text.split('/')
    id_prod = filter(lambda x: x.isnumeric(), url_list)
    try:
        id_prod = list(id_prod)[0]
    except IndexError:
        await msg.answer(text='Не верная ссылка', reply_markup=kb_main_admin)
    prod_info = all_pars(id_prod)
    product_dict.update(prod_info)
    product_dict['min_price'] = prod_info['price']
    product_dict['start_price'] = prod_info['price']
    img_link = img_by_id(id_prod)
    product_dict['photo_link'] = img_link
    print(product_dict)
    if orm.add_product(product_dict):
        await msg.answer_photo(photo=img_link, caption=prod_info['name_prod'], reply_markup=kb_main_admin)
    else:
        await msg.answer(text='Ссылка уже отслеживается', reply_markup=kb_main_admin)


@router.message()
async def eho_admin(msg: types.Message):
    await msg.answer(text='ответcvbcv', reply_markup=kb_main_admin)

# @router.callback_query()
