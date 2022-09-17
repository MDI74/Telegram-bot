from aiogram import types, Dispatcher
from Bot import bot
from keyboards import client_kb, inline
from data_base import sqlite_db


CHANNEL_ID = ["-1001609147352", "-1001744389432"]
NOTSUB_MESSAGE = "Для доступа к функционалу бота, пожалуйста подпишитесь на каналы"
PAGE = 1
ID_MANGA = 0
SORT_TOM = False


#Функция проверка статуса пользователя
def check_sub_channel(chat_member):
    return True if chat_member['status'] != 'left' else False


async def start(message: types.Message):
    check = await sqlite_db.sql_check_user(message.from_user.id)
    if check == []:
        await sqlite_db.sql_add_user(message.from_user.id)
    count_channel = 0
    for channel in CHANNEL_ID:
        if check_sub_channel(await bot.get_chat_member(chat_id=channel, user_id=message.from_user.id)):
            count_channel += 1
    if count_channel == len(CHANNEL_ID):
        try:
           await bot.send_message(message.from_user.id, 'Привет', reply_markup=client_kb.btn_case_client)
        except:
            await message.reply("Напишите ему: @AniAmbry_Manga_Bot")
    else:
        await bot.send_message(message.from_user.id, NOTSUB_MESSAGE, reply_markup=inline.btn_subscribes)


#Фукнция выводящая все меню манги
async def manga_menu(message: types.Message):
    if message.text == "📓 Вся манга":
        global PAGE
        PAGE = 1
        count_channel = 0
        for channel in CHANNEL_ID:
            if check_sub_channel(await bot.get_chat_member(chat_id=channel, user_id=message.from_user.id)):
                count_channel += 1
        if count_channel == len(CHANNEL_ID):
            inline.add_manga(await sqlite_db.sql_read_all_manga(PAGE))
            await bot.send_message(message.from_user.id, f'Список загруженной манги страница {PAGE}', reply_markup=inline.mainmenu)
            await message.delete()
        else:
            await bot.send_message(message.from_user.id, NOTSUB_MESSAGE, reply_markup=inline.btn_subscribes)
    elif message.text == "Привет бот":
        await bot.send_message(message.from_user.id, f'Привет {message.from_user.first_name}')
    else:
        await bot.send_message(message.from_user.id, 'Я не понимаю о чем вы')


#Функция получения id манги
def get_id(id):
    global ID_MANGA
    ID_MANGA = id


#Фукнция обратной связи для манги
async def process_callback_key(call: types.CallbackQuery):
    id = ''.join(call.data.split('key')[:])
    get_id(id)
    name_manga = ''
    id_manga = 0
    read = await sqlite_db.sql_read_id_manga(id)
    for res in read:
        id_manga = res[0]
        name_manga = res[1]
    inline.add_tom(await sqlite_db.sql_read_all_tom(id_manga, PAGE))
    await bot.delete_message(call.from_user.id, call.message.message_id)
    await bot.send_message(call.from_user.id, f'Список загруженной манги {name_manga} cтраница {PAGE}', reply_markup=inline.menumanga)


#Фукнция перелистывания страниц манги
async def process_callback_btn(call: types.CallbackQuery):
    global PAGE
    id = call.data[-1]
    if id == 'R' and PAGE != 50:
        PAGE += 1
    elif id == 'L' and PAGE != 1:
        PAGE -= 1
    await bot.answer_callback_query(call.id)
    inline.add_manga(await sqlite_db.sql_read_all_manga(PAGE))
    await bot.delete_message(call.from_user.id, call.message.message_id)
    await bot.send_message(call.from_user.id, f'Список загруженной манги страница {PAGE}', reply_markup=inline.mainmenu)


#Фукнция перелистывания страниц томов
async def process_callback_btn_tom(call: types.CallbackQuery):
    global PAGE, SORT_TOM
    id_manga = 0
    name_manga = ''
    id = call.data[-1]
    if id == 'R' and PAGE != 50:
        PAGE += 1
    elif id == 'L' and PAGE != 1:
        PAGE -= 1
    elif id == 'S':
        PAGE = 1
    elif id == 'M':
        PAGE = 1
        inline.add_manga(await sqlite_db.sql_read_all_manga(PAGE))
        await bot.delete_message(call.from_user.id, call.message.message_id)
        await bot.send_message(call.from_user.id, f'Список загруженной манги страница {PAGE}', reply_markup=inline.mainmenu)
    if id == 'R' or id == 'L' or id == 'S':
        read = await sqlite_db.sql_read_id_manga(ID_MANGA)
        for res in read:
            id_manga = res[0]
            name_manga = res[1]
        if id == 'S':
            if SORT_TOM:
                SORT_TOM = False
                inline.add_tom(await sqlite_db.sql_read_all_tom(id_manga, PAGE))
            else:
                SORT_TOM = True
                inline.add_tom(await sqlite_db.sql_read_desc_tom(id_manga, PAGE))
        else:
            if SORT_TOM:
                inline.add_tom(await sqlite_db.sql_read_desc_tom(id_manga, PAGE))
            else:
                inline.add_tom(await sqlite_db.sql_read_all_tom(id_manga, PAGE))
        await bot.delete_message(call.from_user.id, call.message.message_id)
        await bot.send_message(call.from_user.id, f'Список загруженных томов {name_manga} cтраница {PAGE}',
                               reply_markup=inline.menumanga)


#Функция проверки подписки
async def checksub(call: types.CallbackQuery):
    count_channel = 0
    await bot.delete_message(call.from_user.id, call.message.message_id)
    for channel in CHANNEL_ID:
        if check_sub_channel(await bot.get_chat_member(chat_id=channel, user_id=call.from_user.id)):
            count_channel += 1
    if count_channel == len(CHANNEL_ID):
        await bot.send_message(call.from_user.id, 'Привет, спасибо за подписку!', reply_markup=client_kb.btn_case_client)
    else:
        await bot.send_message(call.from_user.id, NOTSUB_MESSAGE, reply_markup=inline.btn_subscribes)


def register_handlers_client(dp: Dispatcher):
    dp.register_message_handler(start, commands=['start'])
    dp.register_callback_query_handler(checksub, text=['checksub'])
    dp.register_message_handler(manga_menu, content_types=['text'])
    dp.register_callback_query_handler(process_callback_key, text_contains=['key'])
    dp.register_callback_query_handler(process_callback_btn, text_contains=['btn'])
    dp.register_callback_query_handler(process_callback_btn_tom, text_contains=['button'])








