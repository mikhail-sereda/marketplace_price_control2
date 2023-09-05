import asyncio

from create_bot import bot, dp

from handlers import h_admin, h_user, h_other
from parser1 import parsing_price_thread


async def main() -> None:
    dp.include_router(h_admin.router)
    dp.include_router(h_user.router)
    dp.include_router(h_other.router)
    await bot.delete_webhook(drop_pending_updates=True)
    loop = asyncio.get_event_loop()
    loop.create_task(parsing_price_thread(1))
    await dp.start_polling(bot)


if __name__ == '__main__':

    # loop.create_task(parsing_price2(15))
    asyncio.run(main())
