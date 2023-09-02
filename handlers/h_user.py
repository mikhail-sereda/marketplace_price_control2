from aiogram import Router, types, F
from aiogram.filters import CommandStart
# from aiogram.types import CallbackQuery

from keyboards.kb_user import kb_main_user
from keyboards.ikb_user import gen_markup_pagination, gen_markup_profile
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
    if all_product:
        page_number = 0
        await msg.answer_photo(photo=all_product[page_number].photo_link,
                               caption=f'<a href="{all_product[page_number].link}"><b>{all_product[page_number].name_prod}</b></a>\n\n'
                                       f'<b>Начальная цена: </b>{all_product[page_number].start_price} руб.\n'
                                       f'<b>Минимальная цена: </b>{all_product[page_number].min_price} руб.\n'
                                       f'<b>Текущая цена: </b>{all_product[page_number].price} руб.',
                               reply_markup=await gen_markup_pagination(str(all_product[page_number].id),
                                                                        len(all_product),
                                                                        page_number=page_number))
    else:
        await msg.answer(text=f'У вас нет сохранённых товаров', reply_markup=kb_main_user)


@router.callback_query(lambda x: x.data.startswith('track'))
async def product_pagination(callback: types.CallbackQuery):
    """Обработка кнопокки пагинации моих товаров"""
    inl_col = callback.data.split(':')
    all_product = orm.db_get_user_product(callback.from_user.id)
    page_number = int(inl_col[1])
    photo = types.InputMediaPhoto(media=all_product[page_number].photo_link,
                                  caption=f'<a href="{all_product[page_number].link}"><b>{all_product[page_number].name_prod}</b></a>\n\n'
                                          f'<b>Начальная цена: </b>{all_product[page_number].start_price} руб.\n'
                                          f'<b>Минимальная цена: </b>{all_product[page_number].min_price} руб.\n'
                                          f'<b>Текущая цена: </b>{all_product[page_number].price} руб.')

    await callback.message.edit_media(media=photo,
                                      reply_markup=await gen_markup_pagination(
                                          str(all_product[page_number].id),
                                          len(all_product),
                                          page_number=page_number))


@router.callback_query(lambda x: x.data.startswith('delall'))
async def del_all_product(callback: types.CallbackQuery):
    """Удаление последнего товара"""
    inl_col = callback.data.split(':')
    orm.db_dell_product(int(inl_col[1]))
    await callback.message.delete()
    await callback.answer(text='нет товаров')  # удаляем сообщеие с пагинацией и удаляем последний товар


@router.callback_query(lambda x: x.data.startswith('delpr'))
async def del_product(callback: types.CallbackQuery):
    """Удаление товара если в списке больше однго товара"""
    inl_col = callback.data.split(':')
    orm.db_dell_product(int(inl_col[1]))  # удаляет товар из бд
    all_product = orm.db_get_user_product(callback.from_user.id)
    page_number = int(inl_col[2])
    await callback.answer(text=f'Кнопка', reply_markup=kb_main_user)
    photo = types.InputMediaPhoto(media=all_product[page_number].photo_link,
                                  caption=f'<a href="{all_product[page_number].link}"><b>{all_product[page_number].name_prod}</b></a>\n\n'
                                          f'<b>Начальная цена: </b>{all_product[page_number].start_price} руб.\n'
                                          f'<b>Минимальная цена: </b>{all_product[page_number].min_price} руб.\n'
                                          f'<b>Текущая цена: </b>{all_product[page_number].price} руб.')
    await callback.message.edit_media(media=photo,
                                      reply_markup=await gen_markup_pagination(str(all_product[page_number].id),
                                                                               len(all_product),
                                                                               page_number=page_number))


@router.message(F.text == 'Профиль')
async def get_user_profile(msg: types.Message):
    """Кнопка Профиль"""
    id_user = msg.from_user.id
    profile_user = orm.db_get_profile(id_user)
    count = orm.db_get_count_product_user(id_user)
    await msg.answer(text=f'<b>___Профиль___</b>\n\n'
                          f'<b>Имя: </b>{msg.from_user.first_name}\n'
                          f'<b>ID: </b>{id_user}\n'
                          f'<b>Количество товаров: </b>{count}\n'
                          f'<b>Товаров отслеживается: </b>10\n'
                          f'<b>Тариф: </b>{profile_user.tariff_user}\n'
                          f'<b>Баланс: </b>{profile_user.balance}\n',
                     reply_markup=await gen_markup_profile())
@router.callback_query(lambda x: x.data.startswith('u_tariff'))
async def get_tariff_for_users(callback: types.CallbackQuery):
    active_tariff = orm.db_get_tariffs(1)
    text_farifs = ''
    for text in active_tariff:
        text_farifs += f'<b><u>{text.name_tariff}</u></b>\n\n' \
                       f'До {text.tracked_items} ссылок\n' \
                       f'Стоимость {text.price_tariff} руб.\n' \
                       f'{"➖"*10}\n'
    await callback.message.answer(text=text_farifs)




# @router.message()
# async def eho_user(msg: types.Message):
#     await msg.answer(text='ответ', reply_markup=kb_main_user)
