from aiogram import Router, types, F
from aiogram.filters import CommandStart

from keyboards.kb_user import kb_main_user
from data import orm
from parser1 import img_by_id, all_pars

router: Router = Router()


@router.message(CommandStart())
async def start_other(msg: types.Message):
    """при входе нового пользователя добавляет в БД"""
    orm.db_add_user(msg.from_user.id)
    await msg.answer(text=f'Привет {msg.from_user.first_name}', reply_markup=kb_main_user)


@router.message(F.text=='Помощь')
async def help_all(msg: types.Message):
    """Обрабатывает кнопку помощь для всех пользователей"""    
    await msg.answer(text=f'Помощь {msg.from_user.first_name}', reply_markup=kb_main_user)


@router.message()
async def parsing_link(msg: types.Message):
    """Получает ссылку на wildber выбирает id передаёт парсеру и записывает в бд"""
    product_dict = {'user_id': msg.from_user.id, 'link': msg.text}
    url_list = msg.text.split('/')
    id_prod = filter(lambda x: x.isnumeric(), url_list)
    try:
        id_prod = list(id_prod)[0]
    except IndexError:
        await msg.answer(text='Не верная ссылка')
    prod_info = all_pars(id_prod)
    product_dict.update(prod_info)
    product_dict['min_price'] = prod_info['price']
    product_dict['start_price'] = prod_info['price']
    img_link = img_by_id(id_prod)
    product_dict['photo_link'] = img_link
    print(product_dict)
    if orm.db_add_product(product_dict):
        await msg.answer_photo(photo=img_link, caption=prod_info['name_prod'])
    else:
        await msg.answer(text='Ссылка уже отслеживается')


