import sqlite3

conn = sqlite3.connect('shop.db')

# ???????? ??????????
sql = conn.cursor()



# sql.execute('CREATE TABLE Number (num INTEGER);')

# sql.execute('CREATE TABLE users (telegram_id INTEGER, number TEXT);')
conn.commit()
conn.close()




# Получение названий товаров
def get_products():
    conn = sqlite3.connect('shop.db')

    # Переводчик
    sql = conn.cursor()

    o = sql.execute('SELECT pr_name FROM products')

    return o

# Получение описания товара
def get_about(product_name):
    conn = sqlite3.connect('shop.db')

    # Переводчик
    sql = conn.cursor()

    o = sql.execute(f'SELECT * FROM products WHERE pr_name="{product_name}";')
    conn.commit()

    return o


# Добавляем в корзину товар и количество для определенного пользователя
def add_cart(user_id, product_name, quan):
    conn = sqlite3.connect('shop.db')

    sql = conn.cursor()

    sql.execute(f'INSERT INTO Bara (id, название, количество) VALUES ("{user_id}", "{product_name}", {quan});')
    conn.commit()


# Запись пользователя
def register(user_id, number,name):
    conn = sqlite3.connect('shop.db')

    # Переводчик
    sql = conn.cursor()

    sql.execute(f'INSERT INTO users(telegram_id, number, name) VALUES ({user_id}, "{number}", "{name}");')
    conn.commit()

def register1(user_id, number):
    conn = sqlite3.connect('shop.db')

    # Переводчик
    sql = conn.cursor()

    sql.execute(f'INSERT INTO users(telegram_id, number) VALUES ({user_id}, "{number}");')
    conn.commit()


def number_zakaz():
    conn = sqlite3.connect('shop.db')

    # Переводчик
    sql = conn.cursor()

    sql.execute(f'UPDATE Number SET num = num +1 ;')
    conn.commit()


def number_get_zakaz():
    conn = sqlite3.connect('shop.db')

    # Переводчик
    sql = conn.cursor()

    o = sql.execute(f'SELECT * FROM Number ;')
    conn.commit()

    return o


def his_nuber(user_id):
    conn = sqlite3.connect('shop.db')

    # Переводчик
    sql = conn.cursor()

    o = sql.execute(f'SELECT * FROM users WHERE telegram_id={user_id};')
    conn.commit()

    return o



# Проверка пользователя
def check_user():
    conn = sqlite3.connect('shop.db')

    # Переводчик
    sql = conn.cursor()
    o = sql.execute('SELECT telegram_id FROM users;')

    users = [i[0] for i in o]
    conn.commit()

    return users

# Получить корзину
def get_cart(user_id):
    conn = sqlite3.connect('shop.db')

    # Переводчик
    sql = conn.cursor()

    o = sql.execute(f'SELECT * FROM Bara WHERE id={user_id};')
    conn.commit()

    return o

def Baza():
    conn = sqlite3.connect('shop.db')

    # Переводчик
    sql = conn.cursor()

    o = sql.execute(f'SELECT * FROM products;')
    conn.commit()

    return o

def get_uu(user_id):
    conn = sqlite3.connect('shop.db')

    # Переводчик
    sql = conn.cursor()

    o = sql.execute(f'SELECT * FROM users WHERE telegram_id={user_id};')
    conn.commit()

    return o


def delet_cart(user_id):
    conn = sqlite3.connect('shop.db')

    # Переводчик
    sql = conn.cursor()

    o = sql.execute(f'DELETE FROM Bara WHERE id={user_id};')
    conn.commit()

    return o


def update_name(user_id):
    conn = sqlite3.connect('shop.db')

    # Переводчик
    sql = conn.cursor()

    sql.execute(f'DELETE FROM users WHERE telegram_id={user_id} ;')
    conn.commit()

def update_number(number):
    conn = sqlite3.connect('shop.db')

    # Переводчик
    sql = conn.cursor()

    sql.execute(f'UPDATE users SET number = number {number} ;')
    conn.commit()


def get_fun():
    conn = sqlite3.connect('shop.db')

    # Переводчик
    sql = conn.cursor()

    o = sql.execute(f'SELECT * FROM users;')
    conn.commit()

    return o


