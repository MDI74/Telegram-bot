from aiogram.dispatcher import FSMContext, Dispatcher
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram import types
from aiogram.dispatcher.filters import Text
from Bot import bot
from data_base import sqlite_db
from keyboards import admin_kb, inline
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
import os

ID = None
PAGE = 1
ADMIN_ID = os.getenv('ADMINS')

#Класс машины состоя для загрузки томов
class FSMAdmin(StatesGroup):
    manga = State()
    url = State()
    tom = State()


#Класс машины состоя для загрузки манги
class FSMAdd(StatesGroup):
    manga = State()


async def make_change_command(message: types.Message):
    global ID
    ID = message.from_user.id
    print(ID)
    print(ADMIN_ID)
    if str(ID) in ADMIN_ID:
        await bot.send_message(message.from_user.id, "Приветствую админ", reply_markup=admin_kb.btn_case_admin)
        await message.delete()


#Начало диалога загрузки манги
async def cm_add(message: types.Message):
    if message.from_user.id == ID:
        await FSMAdd.manga.set()
        await message.reply('Введите название манги')


#Функция добавления название манги
async def add_manga(message: types.Message, state: FSMContext):
    if message.from_user.id == ID:
        if message.text == 'отмена':
            await state.finish()
            await message.reply('ОК')
        else:
            async with state.proxy() as data:
                data['manga'] = message.text
            await FSMAdd.next()
            await sqlite_db.sql_add_manga(data)
            await message.reply('Успешно добавлено')
            await state.finish()


#Начало диалога загрузки тома
async def cm_start(message: types.Message):
    if message.from_user.id == ID:
        await FSMAdmin.manga.set()
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
async def load_manga(message: types.Message, state: FSMContext):
    if message.from_user.id == ID:
        id_manga = 0
        inline.add_manga(await sqlite_db.sql_read_all_manga(PAGE))
        read = await sqlite_db.sql_read_name_manga(message.text)
        for ret in read:
            id_manga = ret[0]
        if id_manga == 0:
            await state.finish()
            await message.reply('Такой манги нет в базе данных.')
        else:
            async with state.proxy() as data:
                data['manga'] = id_manga
            await FSMAdmin.next()
            await message.reply("Введите ссылку на том")


#Ловим второй ответ и записываем в словарь
async def load_url(message: types.Message, state: FSMContext):
    if message.from_user.id == ID:
        async with state.proxy() as data:
            data['url'] = message.text
        await FSMAdmin.next()
        await message.reply("Введите том")


#Ловим последний ответ и используем полученные данные
async def load_tom(message: types.Message, state: FSMContext):
    if message.from_user.id == ID:
        async with state.proxy() as data:
            data['tom'] = message.text
        await sqlite_db.sql_add_tom(state)
    await message.reply('Успешно добавлено')
    await state.finish()


#Функция обратной связи удаления манги
async def del_callback_manga(callback_query: types.CallbackQuery):
    await sqlite_db.sql_delete_manga(callback_query.data.replace('del ', ''))
    await callback_query.answer(text=f'{callback_query.data.replace("del ","")} удалена.', show_alert=True)
    await bot.delete_message(callback_query.from_user.id, callback_query.message.message_id)


#Функция обратной связи удаления тома
async def del_callback_tom(callback_query: types.CallbackQuery):
    await sqlite_db.sql_delete_tom(callback_query.data.replace('dtom ', ''))
    await callback_query.answer(text=f'{callback_query.data.replace("dtom ","")} удалена.', show_alert=True)
    await bot.delete_message(callback_query.from_user.id, callback_query.message.message_id)


#Функция удаления манги
async def delete_manga(message: types.Message):
    if message.from_user.id == ID:
        read = await sqlite_db.sql_read_del_manga()
        for ret in read:
            await bot.send_message(message.from_user.id, f'{ret[1]}\n')
            await bot.send_message(message.from_user.id, text="^", reply_markup=InlineKeyboardMarkup().add(InlineKeyboardButton(f'Удалить {ret[1]}', callback_data=f'del {ret[0]}')))


#Функция удаления тома
async def delete_tom(message: types.Message):
    if message.from_user.id == ID:
        read = await sqlite_db.sql_read_del_tom()
        for ret in read:
            await bot.send_message(message.from_user.id, f'{ret[2]}\n, {ret[3]}')
            await bot.send_message(message.from_user.id, text="^", reply_markup=InlineKeyboardMarkup().add(InlineKeyboardButton(f'Удалить {ret[3]}', callback_data=f'dtom {ret[0]}')))


def register_handlers_admin(dp: Dispatcher):
    dp.register_message_handler(cm_add, commands=['новая_манга'], state=None)
    dp.register_message_handler(add_manga, state=FSMAdd.manga)
    dp.register_message_handler(cm_start, commands=['добавить_том'], state=None)
    dp.register_message_handler(cancel_handler, state="*", commands='отмена')
    dp.register_message_handler(cancel_handler, Text(equals='отмена', ignore_case=True), state="*")
    dp.register_message_handler(load_manga, state=FSMAdmin.manga)
    dp.register_message_handler(load_url, state=FSMAdmin.url)
    dp.register_message_handler(load_tom, state=FSMAdmin.tom)
    dp.register_message_handler(make_change_command, commands=['moderator'], is_chat_admin=True)
    dp.register_message_handler(delete_manga, commands=['удалить_мангу'])
    dp.register_message_handler(delete_tom, commands=['удалить_том'])
    dp.register_callback_query_handler(del_callback_manga, lambda x: x.data and x.data.startswith('del'))
    dp.register_callback_query_handler(del_callback_tom, lambda x: x.data and x.data.startswith('dtom'))



