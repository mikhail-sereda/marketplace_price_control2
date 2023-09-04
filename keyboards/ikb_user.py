from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder


async def gen_markup_pagination(id_prod, products_len, page_number=0):
    """Создаёт инлайн клавиатуру пагинации товаров
    page_number-порядковый номер товара, seller_id, trecked-1 отслеживается 0 нет,
    products_len - количество товаров в базе"""

    if products_len == 1:
        return InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text=f'❌Удалить❌', callback_data=f'delall:{id_prod}:{page_number}')],
            [InlineKeyboardButton(text=f'⬅️⬅️⬅️', callback_data='null'),
             InlineKeyboardButton(text=f'{page_number + 1}/{products_len}', callback_data=f'null'),
             InlineKeyboardButton(text=f'➡️➡️➡️', callback_data=f'null')]])

    elif 0 < page_number < products_len - 1:
        return InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text=f'❌Удалить❌', callback_data=f'delpr:{id_prod}:{page_number}')],
            [InlineKeyboardButton(text=f'⬅️⬅️⬅️', callback_data=f'track:{page_number - 1}'),
             InlineKeyboardButton(text=f'{page_number + 1}/{products_len}', callback_data=f'null'),
             InlineKeyboardButton(text=f'➡️➡️➡️', callback_data=f'track:{page_number + 1}')]])
    elif page_number == 0:
        return InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text=f'❌Удалить❌', callback_data=f'delpr:{id_prod}:{page_number}')],
            [InlineKeyboardButton(text=f'⬅️⬅️⬅️', callback_data=f'track:{products_len - 1}'),
             InlineKeyboardButton(text=f'{page_number + 1}/{products_len}', callback_data=f'null'),
             InlineKeyboardButton(text=f'➡️➡️➡️', callback_data=f'track:{page_number + 1}')]])

    elif page_number == products_len - 1:
        return InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text=f'❌Удалить❌', callback_data=f'delpr:{id_prod}:{0}')],
            [InlineKeyboardButton(text=f'⬅️⬅️⬅️', callback_data=f'track:{page_number - 1}'),
             InlineKeyboardButton(text=f'{page_number + 1}/{products_len}', callback_data=f'null'),
             InlineKeyboardButton(text=f'➡️➡️➡️', callback_data=f'track:{0}')]])


async def gen_markup_profile():
    """Создаёт инлайн клавиатуру к профайлу"""
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text=f'Тарифы', callback_data=f'u_tariff'),
         InlineKeyboardButton(text=f'Пополнить баланс', callback_data='money')]])


async def gen_markup_users_tariff(tariffs):
    """Создаёт инлайн клавиатуру из доступных тарифов для пользователя"""
    builder = InlineKeyboardBuilder()
    for tariff in tariffs:
        builder.row(InlineKeyboardButton(text=f'{tariff[0]}',
                                         callback_data=f'plugtariff:{tariff[1]}'), width=1)

    return builder.as_markup()


async def gen_markup_replenishes(user_id):
    """Создаёт инлайн кнопку оплачено"""
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text=f'Оплачено', callback_data=f'pay:{user_id}')]])
