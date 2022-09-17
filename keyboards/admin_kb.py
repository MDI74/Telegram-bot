from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


btn_add_main_menu = KeyboardButton("/Новая_манга")
btn_add_content = KeyboardButton("/Добавить_том")
btn_delete_main_menu = KeyboardButton("/Удалить_мангу")
btn_delete_content = KeyboardButton("/Удалить_том")

btn_case_admin = ReplyKeyboardMarkup(resize_keyboard=True)

btn_case_admin.row(btn_add_main_menu, btn_add_content)
btn_case_admin.row(btn_delete_main_menu, btn_delete_content)
