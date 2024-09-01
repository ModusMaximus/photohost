from asyncio import run
from logging import basicConfig, INFO
from os import getenv

from aiogram import Bot, Dispatcher
from dotenv import find_dotenv, load_dotenv

from src.bot.handlers.admin import admin
from src.bot.handlers.main_logic import user_private_router
from src.bot.handlers.registration import registration
from src.bot.middlewares.db import DataBaseSession
from src.database.engine import create_db, session_maker

load_dotenv(find_dotenv())


async def main():
    await create_db()

    basicConfig(level=INFO)
    bot = Bot(token=getenv('TOKEN'))
    dp = Dispatcher()

    dp.include_router(user_private_router)
    dp.include_router(admin)
    dp.include_router(registration)
    dp.update.middleware(DataBaseSession(session_pool=session_maker))
    # dp.update.middleware(getLastMessage())
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == '__main__':
    try:
        run(main())
    except KeyboardInterrupt:
        print('Bot ended')
