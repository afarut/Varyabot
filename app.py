from loader import bot
import asyncio
import data.db as db
import datetime


if __name__ == '__main__':
    from aiogram import executor
    from handlers import dp

    #dp.loop.create_task(example())
    executor.start_polling(dp)