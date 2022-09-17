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
<<<<<<< HEAD
=======

#executor.start_webhook()
>>>>>>> 1694b4fe3d2a0d2eba9f9ae84f5aa7681c4584fe
