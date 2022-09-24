from aiogram import types, Dispatcher
from Bot import bot
from keyboards import client_kb, inline
from data_base import sqlite_db


CHANNEL_ID = ["-1001609147352", "-1001744389432"] #ID каналов на которые нужно подписаться
NOTSUB_MESSAGE = "Для доступа к функционалу бота, пожалуйста подпишитесь на каналы"
PAGE = 1
ID_MENU_CONT = 0
SORT_CONT = False


#Функция получения id контента на главной странице
def get_id(id):
    global ID_MENU_CONT
    ID_MENU_CONT = id


#Функция проверка статуса пользователя
def check_sub_channel(chat_member):
    return True if chat_member['status'] != 'left' else False


#Функция старта бота, в ней проверяется подписан ли пользователь на необходимые каналы
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


#Фукнция выводящая главную страницу
async def main_menu(message: types.Message):
    if message.text == "📓 Вся манга":
        global PAGE
        PAGE = 1
        count_channel = 0
        for channel in CHANNEL_ID:
            if check_sub_channel(await bot.get_chat_member(chat_id=channel, user_id=message.from_user.id)):
                count_channel += 1
        if count_channel == len(CHANNEL_ID):
            inline.add_main_menu(await sqlite_db.sql_read_all_name(PAGE))
            await bot.send_message(message.from_user.id, f'Список загруженной манги страница {PAGE}', reply_markup=inline.mainmenu)
            await message.delete()
        else:
            await bot.send_message(message.from_user.id, NOTSUB_MESSAGE, reply_markup=inline.btn_subscribes)
    elif message.text == "Привет бот":
        await bot.send_message(message.from_user.id, f'Привет {message.from_user.first_name}')
    else:
        await bot.send_message(message.from_user.id, 'Я не понимаю о чем вы')


#Фукнция обратной связи для заголовков на главной странице
async def callback_main_menu(call: types.CallbackQuery):
    id = ''.join(call.data.split('key')[:])
    get_id(id)
    name_manga = ''
    id_main_c = 0
    read = await sqlite_db.sql_read_id_name(id)
    for res in read:
        id_main_c = res[0]
        name_manga = res[1]
    inline.add_menu_content(await sqlite_db.sql_read_all_content(id_main_c, PAGE))
    await bot.delete_message(call.from_user.id, call.message.message_id)
    await bot.send_message(call.from_user.id, f'Список загруженной манги {name_manga} cтраница {PAGE}', reply_markup=inline.menucontent)


#Фукнция перелистывания страниц главной страницы
async def callback_btn_main_menu(call: types.CallbackQuery):
    global PAGE
    id = call.data[-1]
    if id == 'R' and PAGE != 50:
        PAGE += 1
    elif id == 'L' and PAGE != 1:
        PAGE -= 1
    await bot.answer_callback_query(call.id)
    inline.add_main_menu(await sqlite_db.sql_read_all_name(PAGE))
    await bot.delete_message(call.from_user.id, call.message.message_id)
    await bot.send_message(call.from_user.id, f'Список загруженной манги страница {PAGE}', reply_markup=inline.mainmenu)


#Фукнция перелистывания страниц контента
async def callback_btn_menu_content(call: types.CallbackQuery):
    global PAGE, SORT_CONT
    id_main_c = 0
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
        inline.add_main_menu(await sqlite_db.sql_read_all_name(PAGE))
        await bot.delete_message(call.from_user.id, call.message.message_id)
        await bot.send_message(call.from_user.id, f'Список загруженной манги страница {PAGE}', reply_markup=inline.mainmenu)
    if id == 'R' or id == 'L' or id == 'S':
        read = await sqlite_db.sql_read_id_name(ID_MENU_CONT)
        for res in read:
            id_main_c = res[0]
            name_manga = res[1]
        if id == 'S':
            if SORT_CONT:
                SORT_CONT = False
                inline.add_menu_content(await sqlite_db.sql_read_all_content(id_main_c, PAGE))
            else:
                SORT_CONT = True
                inline.add_menu_content(await sqlite_db.sql_read_desc_content(id_main_c, PAGE))
        else:
            if SORT_CONT:
                inline.add_menu_content(await sqlite_db.sql_read_desc_content(id_main_c, PAGE))
            else:
                inline.add_menu_content(await sqlite_db.sql_read_all_content(id_main_c, PAGE))
        await bot.delete_message(call.from_user.id, call.message.message_id)
        await bot.send_message(call.from_user.id, f'Список загруженных томов {name_manga} cтраница {PAGE}', reply_markup=inline.menucontent)


#Функция проверки на подписку
async def check_sub(call: types.CallbackQuery):
    count_channel = 0
    await bot.delete_message(call.from_user.id, call.message.message_id)
    for channel in CHANNEL_ID:
        if check_sub_channel(await bot.get_chat_member(chat_id=channel, user_id=call.from_user.id)):
            count_channel += 1
    if count_channel == len(CHANNEL_ID):
        await bot.send_message(call.from_user.id, 'Привет, спасибо за подписку!', reply_markup=client_kb.btn_case_client)
    else:
        await bot.send_message(call.from_user.id, NOTSUB_MESSAGE, reply_markup=inline.btn_subscribes)


#Регистрация хэндлеров клиента
def register_handlers_client(dp: Dispatcher):
    dp.register_message_handler(start, commands=['start'])
    dp.register_callback_query_handler(check_sub, text=['checksub'])
    dp.register_message_handler(main_menu, content_types=['text'])
    dp.register_callback_query_handler(callback_main_menu, text_contains=['key'])
    dp.register_callback_query_handler(callback_btn_main_menu, text_contains=['btn'])
    dp.register_callback_query_handler(callback_btn_menu_content, text_contains=['button'])








