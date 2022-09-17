from aiogram.utils import executor
from Bot import dp
from handlers import client, admin
from data_base import sqlite_db


async def on_startup(_):
    print("Бот запущен")
    sqlite_db.sql_start()

admin.register_handlers_admin(dp)
client.register_handlers_client(dp)

executor.start_polling(dp, skip_updates=True, on_startup=on_startup) #skip_updates=True, чтобы бот не отвечал на сообщения которые были отправлены когда бот не работал

executor.start_webhook()