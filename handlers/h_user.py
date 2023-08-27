from aiogram import Router, types
from aiogram.filters import CommandStart

from keyboards.kb_user import kb_main_user
from filters.my_filter import UserFilt

from data import orm



router: Router = Router()


@router.message(UserFilt(), CommandStart())
async def start_user(msg: types.Message):
    """При входе зарегистрированого пользователя проверяет данные в БД"""
    orm.add_user(msg.from_user.id)
    await msg.answer(text=f'Привет {msg.from_user.first_name}', reply_markup=kb_main_user)


#
# @router.message()
# async def user_products(msg: types.Message):
#     """Кнопка Мои товары"""
#     pass
#
# @router.message()
# async def user_profile(msg: types.Message):
#     """Кнопка профиль"""
#     pass
#
# @router.message()
# async def user_useful(msg: types.Message):
#     """Кнопка полезное"""
#     pass
#
# @router.message()
# async def user_help(msg: types.Message):
#     """Кнопка Мои товары"""
#     pass

@router.message()
async def eho_user(msg: types.Message):
    await msg.answer(text='ответ', reply_markup=kb_main_user)
