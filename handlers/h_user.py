from aiogram import Router, types, F
from aiogram.filters import CommandStart

from keyboards.kb_user import kb_main_user
from filters.my_filter import UserFilt

from data import orm

router: Router = Router()


@router.message(UserFilt(), CommandStart())
async def start_user(msg: types.Message):
    """При входе зарегистрированого пользователя проверяет данные в БД"""
    orm.db_add_user(msg.from_user.id)
    await msg.answer(text=f'Привет {msg.from_user.first_name}', reply_markup=kb_main_user)


@router.message(F.text == 'Мои товары')
async def user_products(msg: types.Message):
    """Кнопка Мои товары"""
    all_product = orm.db_get_user_product(msg.from_user.id)
    num = 0
    await msg.answer(text=f'Кнопка', reply_markup=kb_main_user)

    await msg.answer_photo(photo=all_product[num].photo_link,
                           caption=f'<a href="{all_product[num].link}"><b>{all_product[num].name_prod}</b></a>\n\n'
                                   f'<b>Начальная цена: </b>{all_product[num].start_price} руб.\n'
                                   f'<b>Минимальная цена: </b>{all_product[num].min_price} руб.\n'
                                   f'<b>Текущая цена: </b>{all_product[num].price} руб.')


@router.message(F.text == 'Профиль')
async def user_profile(msg: types.Message):
    """Кнопка Профиль"""
    profile_user = orm.db_get_profile(msg.from_user.id)
    print(profile_user.tariff_user)

    await msg.answer(text=f'<b>___Профиль___</b>\n\n'
                          f'<b>Имя: </b>{msg.from_user.first_name}\n'
                          f'<b>ID: </b>{profile_user.user_id}\n'
                          f'<b>Количество товаров: </b>10\n'
                          f'<b>Товаров отслеживается: </b>10\n'
                          f'<b>Тариф: </b>{profile_user.tariff_user}\n'
                          f'<b>Баланс: </b>{profile_user.balance}\n')

# @router.message()
# async def user_help(msg: types.Message):
#     """Кнопка Мои товары"""
#     pass

# @router.message()
# async def eho_user(msg: types.Message):
#     await msg.answer(text='ответ', reply_markup=kb_main_user)
