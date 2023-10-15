import asyncio
import threading

from data import orm
from create_bot import bot


async def checking_tariff_user():
    users = orm.db_get_all_users()
    print(users)
    for user in users:
        orm.db_changes_user_tariff(name_tariff='Стандартный',
                                   id_user=user.user_id,
                                   tracked_items=3,
                                   balance=user.balance)
        await bot.send_message(chat_id=user.user_id, text=f'Действие тарифа {user.tariff_user} закончено.\n'
                                                          f'Вам подключен тариф Стандартный. Отслеживается 3 ссылки.')
        print(user.user_id)


async def checking_tariff_thread(wait_for):
    """Запускает новый поток для проверки тарифа у пользователей"""
    while True:
        await asyncio.sleep(wait_for)
        check = threading.Thread(target=await checking_tariff_user())
        check.start()
