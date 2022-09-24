from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

list_keys = []


#Класс для очищения inlinekeyboardmarkup
class InlineKeyboardMarkupWithClear(InlineKeyboardMarkup):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def add(self, *args):
        self.inline_keyboard.clear()
        return super().add(*args)


#Функция добавления кнопок с заголовком в главное меню
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


#Функция добаления кнопок для выбора удаления заголовка
def del_main_menu(res):
    global list_keys
    list_keys = []
    for i in res:
        keys = InlineKeyboardButton(row_width=1, text=i[1], callback_data=f'delmain {i[0]}')
        list_keys.append(keys)
    delmainmenu.add(*list_keys).row(delmainkeyL, delmainkeyM, delmainkeyR)


#Функция добаления кнопок для выбора контенат заголовка для удаления
def del_content_main_menu(res):
    global list_keys
    list_keys = []
    for i in res:
        keys = InlineKeyboardButton(row_width=1, text=i[1], callback_data=f'delmaincontent {i[0]}')
        list_keys.append(keys)
    delcontentmainmenu.add(*list_keys).row(delcontmainkeyL, delcontmainkeyM, delcontmainkeyR)


#Функция добаления кнопок для выбора контента для удаления
def del_content(res):
    global list_keys
    list_keys = []
    for i in res:
        keys = InlineKeyboardButton(row_width=1, text=i[3], callback_data=f'delcontent {i[0]}')
        list_keys.append(keys)
    delcontent.add(*list_keys).row(delcontkeyL, delcontkeyM, delcontkeyR).row(delcontkeyS)


mainmenu = InlineKeyboardMarkupWithClear(row_width=1)
menucontent = InlineKeyboardMarkupWithClear(row_width=1)

delmainmenu = InlineKeyboardMarkupWithClear(row_width=1)

delcontentmainmenu = InlineKeyboardMarkupWithClear(row_width=1)
delcontent = InlineKeyboardMarkupWithClear(row_width=1)


#Кнопки для перелистывания страниц на главной старницы
keyL = InlineKeyboardButton(row_width=3, text='⬅️', callback_data='btnL')
keyM = InlineKeyboardButton(row_width=3, text='⏹', callback_data='None')
keyR = InlineKeyboardButton(row_width=3, text='➡️', callback_data='btnR')


#Кнопки для перелистывания страниц на страницы с контентом
content_keyL = InlineKeyboardButton(row_width=3, text='⬅️', callback_data='buttonL')
content_keyM = InlineKeyboardButton(row_width=3, text='⏹ Вся манга`', callback_data='buttonM')
content_keyR = InlineKeyboardButton(row_width=3, text='➡️', callback_data='buttonR')
content_keyS = InlineKeyboardButton(row_width=3, text='🔃 В конец/начало', callback_data='buttonS')


#Кнопки для перелистывания страниц в меню удаления кнопки заголовка
delmainkeyL = InlineKeyboardButton(row_width=3, text='⬅️', callback_data='delmainbtnL')
delmainkeyM = InlineKeyboardButton(row_width=3, text='Отмена', callback_data='delmainbtnM')
delmainkeyR = InlineKeyboardButton(row_width=3, text='➡️', callback_data='delmainbtnR')


#Кнопки для перелистывания страниц в главном меню выбора контента заголовка для удаления
delcontmainkeyL = InlineKeyboardButton(row_width=3, text='⬅️', callback_data='delmaincontbtnL')
delcontmainkeyM = InlineKeyboardButton(row_width=3, text='Отмена', callback_data='delmaincontbtnM')
delcontmainkeyR = InlineKeyboardButton(row_width=3, text='➡️', callback_data='delmaincontbtnR')


#Кнопки для перелистывания страниц в главном меню выбора контента заголовка для удаления
delcontkeyL = InlineKeyboardButton(row_width=3, text='⬅️', callback_data='delcontbtnL')
delcontkeyM = InlineKeyboardButton(row_width=3, text='⏹ Вся манга', callback_data='delcontbtnM')
delcontkeyR = InlineKeyboardButton(row_width=3, text='➡️', callback_data='delcontbtnR')
delcontkeyS = InlineKeyboardButton(row_width=3, text='🔃 В конец/начало', callback_data='delcontbtnS')

#Кнопки ведущие к каналам на которые необходимо подписаться
btn_subscribes = InlineKeyboardMarkup(row_width=1)
btn_sub1 = InlineKeyboardButton(text="AniAmbry | Манга", url="https://t.me/mdi7444")
btn_sub2 = InlineKeyboardButton(text="AniAmbry | Picture", url="https://t.me/MDI755")
btn_check_sub = InlineKeyboardButton(text="Проверить 🔐", callback_data='checksub')

btn_subscribes.add(btn_sub1, btn_sub2, btn_check_sub)




