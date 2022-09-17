from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

btn_add_manga = KeyboardButton("/Новая_манга")
btn_add = KeyboardButton("/Добавить_том")
btn_delete = KeyboardButton("/Удалить_мангу")
btn_delete_tom = KeyboardButton("/Удалить_том")

btn_case_admin = ReplyKeyboardMarkup(resize_keyboard=True)

btn_case_admin.row(btn_add_manga, btn_add)
btn_case_admin.row(btn_delete, btn_delete_tom)
