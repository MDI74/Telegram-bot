from aiogram.dispatcher import FSMContext, Dispatcher
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram import types
from aiogram.dispatcher.filters import Text
from Bot import bot
from data_base import sqlite_db
from keyboards import admin_kb, inline
import os

ID = None
PAGE = 1
ADMIN_ID = os.getenv('ADMINS')
SORT_CONT = False
ID_MENU_CONT = 0


#Функция получения id контента на главной странице
def get_id(id):
    global ID_MENU_CONT
    ID_MENU_CONT = id


#Класс машины состояния для загрузки контента
class FSMAddMainContent(StatesGroup):
    name_main = State()
    content_url = State()
    content_desc = State()


#Класс машины состояния для загрузки название на главную страницу
class FSMAddContent(StatesGroup):
    name_main = State()


#Функция проверки на администратора
async def make_change_command(message: types.Message):
    global ID
    ID = message.from_user.id
    if str(ID) in ADMIN_ID:
        await bot.send_message(message.from_user.id, "Приветствую админ", reply_markup=admin_kb.btn_case_admin)
        await message.delete()


#Начало диалога загрузки названия на главную страницу
async def cm_add(message: types.Message):
    if message.from_user.id == ID:
        await FSMAddContent.name_main.set()
        await message.reply('Введите название манги')


#Функция добавления название в главное меню
async def add_main_menu(message: types.Message, state: FSMContext):
    if message.from_user.id == ID:
        if message.text == 'отмена':
            await state.finish()
            await message.reply('ОК')
        else:
            async with state.proxy() as data:
                data['manga'] = message.text
            await FSMAddContent.next()
            await sqlite_db.sql_add_name(data)
            await message.reply('Успешно добавлено')
            await state.finish()


#Начало диалога загрузки контент
async def cm_start(message: types.Message):
    if message.from_user.id == ID:
        await FSMAddMainContent.name_main.set()
        await message.reply('Введите название манги')


#Функция отмены добавления или удаления
async def cancel_handler(message: types.Message, state: FSMContext):
    if message.from_user.id == ID:
        current_state = await state.get_state()
        if current_state is None:
            return
        await state.finish()
        await message.reply('ОК')


#Ловим первый ответ и записываем в словарь
async def load_name_main(message: types.Message, state: FSMContext):
    if message.from_user.id == ID:
        id_manga = 0
        inline.add_main_menu(await sqlite_db.sql_read_all_name(PAGE))
        read = await sqlite_db.sql_read_name_main_content(message.text)
        for ret in read:
            id_manga = ret[0]
        if id_manga == 0:
            await state.finish()
            await message.reply('Такой манги нет в базе данных.')
        else:
            async with state.proxy() as data:
                data['manga'] = id_manga
            await FSMAddMainContent.next()
            await message.reply("Введите ссылку на том")


#Ловим второй ответ и записываем в словарь
async def load_content_url(message: types.Message, state: FSMContext):
    if message.from_user.id == ID:
        async with state.proxy() as data:
            data['url'] = message.text
        await FSMAddMainContent.next()
        await message.reply("Введите том")


#Ловим последний ответ и используем полученные данные
async def load_content_desc(message: types.Message, state: FSMContext):
    if message.from_user.id == ID:
        async with state.proxy() as data:
            data['tom'] = message.text
        await sqlite_db.sql_add_content(state)
    await message.reply('Успешно добавлено')
    await state.finish()


#Функция обратной связи удаления заголовка в главном меню
async def del_callback_main_menu(callback_query: types.CallbackQuery):
    await sqlite_db.sql_delete_name(callback_query.data.replace('delmain ', ''))
    await callback_query.answer(text='Удаление прошло успешно.', show_alert=True)
    await bot.delete_message(callback_query.from_user.id, callback_query.message.message_id)


#Функция удаления заголовка в главном меню
async def delete_main_menu(message: types.Message):
    if message.from_user.id == ID:
        inline.del_main_menu(await sqlite_db.sql_read_all_name(PAGE))
        await bot.send_message(message.from_user.id,f'Выберите что удалить страница {PAGE}', reply_markup=inline.delmainmenu)


#Функция перелистывания страниц в главном меню при удалении
async def callback_delbtn_main_menu(call: types.CallbackQuery):
    global PAGE
    id = call.data[-1]
    if id == 'R' and PAGE != 50:
        PAGE += 1
    elif id == 'L' and PAGE != 1:
        PAGE -= 1
    elif id == 'M':
        await bot.delete_message(call.from_user.id, call.message.message_id)
    if id == 'R' or id =='L':
        await bot.answer_callback_query(call.id)
        inline.del_main_menu(await sqlite_db.sql_read_all_name(PAGE))
        await bot.delete_message(call.from_user.id, call.message.message_id)
        await bot.send_message(call.from_user.id, f'Выберите что удалить страница {PAGE}', reply_markup=inline.delmainmenu)


#Функция обратной связи для удаления выбранного контента
async def del_callback_content(callback_query: types.CallbackQuery):
    await sqlite_db.sql_delete_content(callback_query.data.replace('delcontent ', ''))
    await callback_query.answer(text='Удаление прошло успешно.', show_alert=True)
    await bot.delete_message(callback_query.from_user.id, callback_query.message.message_id)


#Функция удаления контента
async def delete_content(message: types.Message):
    if message.from_user.id == ID:
        inline.del_content_main_menu(await sqlite_db.sql_read_all_name(PAGE))
        await bot.send_message(message.from_user.id, f'Выберите что удалить страница {PAGE}', reply_markup=inline.delcontentmainmenu)


#Функция перелистывания страниц в главном меню при удалении контента
async def callback_del_contbtn_main_menu(call: types.CallbackQuery):
    global PAGE
    id = call.data[-1]
    if id == 'R' and PAGE != 50:
        PAGE += 1
    elif id == 'L' and PAGE != 1:
        PAGE -= 1
    elif id == 'M':
        await bot.delete_message(call.from_user.id, call.message.message_id)
    if id == 'R' or id =='L':
        await bot.answer_callback_query(call.id)
        inline.del_content_main_menu(await sqlite_db.sql_read_all_name(PAGE))
        await bot.delete_message(call.from_user.id, call.message.message_id)
        await bot.send_message(call.from_user.id, f'Выберите что удалить страница {PAGE}', reply_markup=inline.delcontentmainmenu)


#Функция обратной связи для кнопок главномого меню при удалении контента
async def callback_delcontmain_menu(call: types.CallbackQuery):
    id = ''.join(call.data.split('delmaincontent')[:])
    get_id(id)
    name_manga = ''
    id_main_c = 0
    read = await sqlite_db.sql_read_id_name(id)
    for res in read:
        id_main_c = res[0]
        name_manga = res[1]
    inline.del_content(await sqlite_db.sql_read_all_content(id_main_c, PAGE))
    await bot.delete_message(call.from_user.id, call.message.message_id)
    await bot.send_message(call.from_user.id, f'Выберите что удалить в {name_manga} cтраница {PAGE}', reply_markup=inline.delcontent)


#Функция для перелистывания страниц в меню контента при удалении контента
async def callback_delbtn_menu_content(call: types.CallbackQuery):
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
        inline.del_content_main_menu(await sqlite_db.sql_read_all_name(PAGE))
        await bot.delete_message(call.from_user.id, call.message.message_id)
        await bot.send_message(call.from_user.id, f'Выберите что удалить страница {PAGE}', reply_markup=inline.delcontentmainmenu)
    if id == 'R' or id == 'L' or id == 'S':
        read = await sqlite_db.sql_read_id_name(ID_MENU_CONT)
        for res in read:
            id_main_c = res[0]
            name_manga = res[1]
        if id == 'S':
            if SORT_CONT:
                SORT_CONT = False
                inline.del_content(await sqlite_db.sql_read_all_content(id_main_c, PAGE))
            else:
                SORT_CONT = True
                inline.del_content(await sqlite_db.sql_read_desc_content(id_main_c, PAGE))
        else:
            if SORT_CONT:
                inline.del_content(await sqlite_db.sql_read_desc_content(id_main_c, PAGE))
            else:
                inline.del_content(await sqlite_db.sql_read_all_content(id_main_c, PAGE))
        await bot.delete_message(call.from_user.id, call.message.message_id)
        await bot.send_message(call.from_user.id, f'Выберите что удалить в {name_manga} cтраница {PAGE}', reply_markup=inline.delcontent)


#Регистрация хэндлеров администратора
def register_handlers_admin(dp: Dispatcher):
    dp.register_message_handler(cm_add, commands=['новая_манга'], state=None)
    dp.register_message_handler(add_main_menu, state=FSMAddContent.name_main)
    dp.register_message_handler(cm_start, commands=['добавить_том'], state=None)
    dp.register_message_handler(cancel_handler, state="*", commands='отмена')
    dp.register_message_handler(cancel_handler, Text(equals='отмена', ignore_case=True), state="*")
    dp.register_message_handler(load_name_main, state=FSMAddMainContent.name_main)
    dp.register_message_handler(load_content_url, state=FSMAddMainContent.content_url)
    dp.register_message_handler(load_content_desc, state=FSMAddMainContent.content_desc)
    dp.register_message_handler(make_change_command, commands=['moderator'], is_chat_admin=True)
    dp.register_message_handler(delete_main_menu, commands=['удалить_мангу'])
    dp.register_message_handler(delete_content, commands=['удалить_том'])
    dp.register_callback_query_handler(callback_delbtn_main_menu, text_contains=['delmainbtn'])
    dp.register_callback_query_handler(callback_del_contbtn_main_menu, text_contains=['delmaincontbtn'])
    dp.register_callback_query_handler(callback_delcontmain_menu, text_contains=['delmaincontent'])
    dp.register_callback_query_handler(callback_delbtn_menu_content, text_contains=['delcontbtn'])
    dp.register_callback_query_handler(del_callback_main_menu, lambda x: x.data and x.data.startswith('delmain'))
    dp.register_callback_query_handler(del_callback_content, lambda x: x.data and x.data.startswith('delcontent'))



