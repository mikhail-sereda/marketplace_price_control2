from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


async def gen_markup_category_tariff():
    return InlineKeyboardMarkup(
        inline_keyboard=[[InlineKeyboardButton(text=f'Активные', callback_data=f'tariff_active:1'),
                          InlineKeyboardButton(text=f'Не активные', callback_data=f'tariff_active:0')],
                          [InlineKeyboardButton(text=f'Добавить тариф', callback_data=f'add_tariff')]])
