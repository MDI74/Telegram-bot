from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

list_keys = []


#Класс для очищения inlinekeyboardmarkup
class InlineKeyboardMarkupWithClear(InlineKeyboardMarkup):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def add(self, *args):
        self.inline_keyboard.clear()
        return super().add(*args)


#Функция добавления кнопок в главное меню
def add_main_menu(res):
    global list_keys
    list_keys = []
    for i in res:
        keys = InlineKeyboardButton(row_width=1, text=i[1], callback_data=f'key{i[0]}')
        list_keys.append(keys)
    mainmenu.add(*list_keys).row(keyL, keyM, keyR)


#Функция добавления кнопок с контентом
def add_menu_content(res):
    global list_keys
    list_keys = []
    for i in res:
        keys = InlineKeyboardButton(row_width=1, text=i[3],  url=i[2], callback_data=f'tom{i[0]}')
        list_keys.append(keys)
    menucontent.add(*list_keys).row(tom_keyL, tom_keyM, tom_keyR).row(tom_keyS)


mainmenu = InlineKeyboardMarkupWithClear(row_width=1)
menucontent = InlineKeyboardMarkupWithClear(row_width=1)


#Кнопки для перелистывения страниц на главной старницы
keyL = InlineKeyboardButton(row_width=3, text='⬅️', callback_data='btnL')
keyM = InlineKeyboardButton(row_width=3, text='⏹', callback_data='b')
keyR = InlineKeyboardButton(row_width=3, text='➡️', callback_data='btnR')


#Кнопки для перелистывения страниц на страницы с контентом
tom_keyL = InlineKeyboardButton(row_width=3, text='⬅️', callback_data='buttonL')
tom_keyM = InlineKeyboardButton(row_width=3, text='⏹ Вся манга', callback_data='buttonM')
tom_keyR = InlineKeyboardButton(row_width=3, text='➡️', callback_data='buttonR')
tom_keyS = InlineKeyboardButton(row_width=3, text='🔃 В конец/начало', callback_data='buttonS')


# Каналы на которые необходимо подписаться
btn_subscribes = InlineKeyboardMarkup(row_width=1)
btn_sub1 = InlineKeyboardButton(text="AniAmbry | Манга", url="https://t.me/mdi7444")
btn_sub2 = InlineKeyboardButton(text="AniAmbry | Picture", url="https://t.me/MDI755")
btn_check_sub = InlineKeyboardButton(text="Проверить 🔐", callback_data='checksub')

btn_subscribes.add(btn_sub1, btn_sub2, btn_check_sub)




