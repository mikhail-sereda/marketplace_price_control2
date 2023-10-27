import asyncio
import threading

from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from data import orm
from create_bot import bot


async def checking_tariff_user():
    users = orm.db_get_all_users_stop_tariff()
    for user in users:
        orm.db_changes_user_tariff(name_tariff='Стандартный',
                                   id_user=user.user_id,
                                   tracked_items=3,
                                   balance=user.balance)
        orm.db_disables_product_tracking(id_user=user.user_id)
        await bot.send_message(chat_id=user.user_id, text=f'Действие тарифа {user.tariff_user} закончено.\n'
                                                          f'Вам подключен тариф Стандартный. Отслеживается 3 ссылки.')


async def checking_tariff_thread(wait_for):
    """Запускает новый поток для проверки тарифа у пользователей"""
    while True:
        await asyncio.sleep(wait_for)
        check = threading.Thread(target=await checking_tariff_user())
        check.start()


async def sends_ads():
    """Пересылает объявление всем активным пользователям"""
    users = orm.db_get_activ_users()
    ad = orm.db_get_ad()
    for user in users:
        try:
            await bot.send_photo(chat_id=user[0], photo=ad.img, caption=ad.text,
                                 reply_markup=InlineKeyboardMarkup(inline_keyboard=[
                                     [InlineKeyboardButton(text=f'{ad.button_name}', url=f'{ad.button}')]]))
        except:
            orm.db_changes_user_activ(id_user=user[0], activ=0)
