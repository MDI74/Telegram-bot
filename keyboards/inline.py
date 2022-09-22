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
        keys = InlineKeyboardButton(row_width=1, text=i[3],  url=i[2], callback_data=f'keycontent{i[0]}')
        list_keys.append(keys)
    menucontent.add(*list_keys).row(content_keyL, content_keyM, content_keyR).row(content_keyS)


def del_main_menu(res):
    global list_keys
    list_keys = []
    for i in res:
        keys = InlineKeyboardButton(row_width=1, text=i[1], callback_data=f'del {i[0]}')
        list_keys.append(keys)
    delmainmenu.add(*list_keys).row(delkeyL, delkeyM, delkeyR)


def del_menu_content(res):
    global list_keys
    list_keys = []
    for i in res:
        keys = InlineKeyboardButton(row_width=1, text=i[3], url=i[2], callback_data=f'keycontent{i[0]}')
        list_keys.append(keys)
    delmenucontent.add(*list_keys).row(del_content_keyL, del_content_keyM, del_content_keyR).row(del_content_keyS)


mainmenu = InlineKeyboardMarkupWithClear(row_width=1)
menucontent = InlineKeyboardMarkupWithClear(row_width=1)

delmainmenu = InlineKeyboardMarkupWithClear(row_width=1)
delmenucontent = InlineKeyboardMarkupWithClear(row_width=1)

#Кнопки для перелистывения страниц на главной старницы
keyL = InlineKeyboardButton(row_width=3, text='⬅️', callback_data='btnL')
keyM = InlineKeyboardButton(row_width=3, text='⏹', callback_data='None')
keyR = InlineKeyboardButton(row_width=3, text='➡️', callback_data='btnR')


#Кнопки для перелистывения страниц на страницы с контентом
content_keyL = InlineKeyboardButton(row_width=3, text='⬅️', callback_data='buttonL')
content_keyM = InlineKeyboardButton(row_width=3, text='⏹ Вся манга', callback_data='buttonM')
content_keyR = InlineKeyboardButton(row_width=3, text='➡️', callback_data='buttonR')
content_keyS = InlineKeyboardButton(row_width=3, text='🔃 В конец/начало', callback_data='buttonS')


#Кнопки для перелистывения страниц на главной старницы
delkeyL = InlineKeyboardButton(row_width=3, text='⬅️', callback_data='delbtnL')
delkeyM = InlineKeyboardButton(row_width=3, text='Отмена', callback_data='delbtnM')
delkeyR = InlineKeyboardButton(row_width=3, text='➡️', callback_data='delbtnR')


del_content_keyL = InlineKeyboardButton(row_width=3, text='⬅️', callback_data='delbuttonL')
del_content_keyM = InlineKeyboardButton(row_width=3, text='⏹ Вся манга', callback_data='delbuttonM')
del_content_keyR = InlineKeyboardButton(row_width=3, text='➡️', callback_data='delbuttonR')
del_content_keyS = InlineKeyboardButton(row_width=3, text='🔃 В конец/начало', callback_data='delbuttonS')



# Каналы на которые необходимо подписаться
btn_subscribes = InlineKeyboardMarkup(row_width=1)
btn_sub1 = InlineKeyboardButton(text="AniAmbry | Манга", url="https://t.me/mdi7444")
btn_sub2 = InlineKeyboardButton(text="AniAmbry | Picture", url="https://t.me/MDI755")
btn_check_sub = InlineKeyboardButton(text="Проверить 🔐", callback_data='checksub')

btn_subscribes.add(btn_sub1, btn_sub2, btn_check_sub)




