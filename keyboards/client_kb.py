from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove

btn1 = KeyboardButton("📓 Вся манга")


btn_case_client = ReplyKeyboardMarkup(resize_keyboard=True)

btn_case_client.row(btn1)


