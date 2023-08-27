import asyncio

from aiogram import Bot, Dispatcher
from dotenv import dotenv_values

from handlers import h_admin, h_user


config = dotenv_values(".env", encoding="utf-8")


TOKEN = config['TOKEN']



async def main() -> None:
    dp: Dispatcher = Dispatcher()
    bot = Bot(token=TOKEN, parse_mode='HTML')

    dp.include_router(h_admin.router)
    dp.include_router(h_user.router)

    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == '__main__':
    # loop = asyncio.get_event_loop()
    # loop.create_task(parsing_price(10))
    # loop.create_task(parsing_price2(15))
    asyncio.run(main())
