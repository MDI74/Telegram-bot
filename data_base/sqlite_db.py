import sqlite3 as sq


#Функция расчета вывода контента в зависимости страниц
def page_list(page):
    return str((page-1)*8), str(8)


#Функция подлючения к базе данных и создание таблиц
def sql_start():
    global base, cur
    base = sq.connect('list_manga.db')
    cur = base.cursor()
    if base:
        print('Data base connected OK!')
    base.execute('CREATE TABLE IF NOT EXISTS manga_list(id INTEGER PRIMARY KEY, name TEXT)')
    base.execute('CREATE TABLE IF NOT EXISTS tom_list(id INTEGER PRIMARY KEY, id_manga INTEGER, url TEXT, tom TEXT)')
    base.execute('CREATE TABLE IF NOT EXISTS users_list(id INTEGER PRIMARY KEY, id_user INTEGER )')
    base.commit()


#Функция добавления названия для кнопки на главной странице в базу данных
async def sql_add_name(data):
    cur.execute('INSERT INTO manga_list(name) VALUES (?)',  tuple(data.values()))
    base.commit()


#Функция добавления id пользователя в базу данных
async def sql_add_user(data):
    cur.execute('INSERT INTO users_list(id_user) VALUES (?)',(data,) )
    base.commit()


#Функция проверки на то что есть ли id в базе данных
async def sql_check_user(id):
    return cur.execute(f'SELECT * FROM users_list WHERE id_user =={id}').fetchall()


#Функция добавления контента в базу данных
async def sql_add_content(state):
    async with state.proxy() as data:
        cur.execute('INSERT INTO tom_list(id_manga,url,tom) VALUES (?,?,?)', tuple(data.values()))
        base.commit()


#Функция получения всего контента из базы данных
async def sql_read_all_name(page):
    id_start, id_end = page_list(page)
    return cur.execute(f'SELECT * FROM manga_list LIMIT {id_start}, {id_end}').fetchall()


#Функция получения id названия из главной странице
async def sql_read_id_name(id):
    return cur.execute(f'SELECT * FROM manga_list WHERE id =={id}').fetchall()


#Функция удаления названия на главной странице из базы данных
async def sql_delete_name(data):
    cur.execute('DELETE FROM manga_list WHERE id == ?', (data,))
    cur.execute('DELETE FROM tom_list WHERE id_manga == ?', (data,))
    base.commit()

#Функция получения названия контента на главной странице из базы данных
async def sql_read_name_main_content(id):
    return cur.execute(f'SELECT * FROM manga_list WHERE name == ?', (id,)).fetchall()


#Функция получения всего контента из базы данных
async def sql_read_all_content(id, page):
    id_start, id_end = page_list(page)
    return cur.execute(f'SELECT * FROM tom_list WHERE id_manga=={id} ORDER BY id LIMIT {id_start}, {id_end}').fetchall()


#Функция удаления контента из базы данных
async def sql_delete_content(data):
    cur.execute('DELETE FROM tom_list WHERE id == ?', (data,))
    base.commit()


#Функция для сортировки контента по убыванию
async def sql_read_desc_content(id, page):
    id_start, id_end = page_list(page)
    return cur.execute(
        f'SELECT * FROM tom_list WHERE id_manga=={id} ORDER BY id DESC LIMIT {id_start}, {id_end}').fetchall()