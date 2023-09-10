import asyncio
import threading

from data import orm


def checking_tariff_user():
    users = orm.db_get_all_users()
    print(users)
    for user in users:
        print(user.user_id)


async def checking_tariff_thread(wait_for):
    """Запускает новый поток для проверки тарифа у пользователей"""
    while True:
        await asyncio.sleep(wait_for)
        check = threading.Thread(target=checking_tariff_user)
        check.start()
