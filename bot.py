import telebot
from telebot import types
import requests
import data

bot = telebot.TeleBot('5226037552:AAHDSCfeWaw5yTcfExeQozhoGf7vZtD9gi4')

users = {}

@bot.message_handler(commands=['start'])
def start(message):
    # Функция для проверки user_id в базе
    user = data.check_user()

    user_id = message.from_user.id

    d = message.from_user.first_name

    # Если user_id нет в базе
    if user_id not in user:
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)

        contact = types.KeyboardButton(text="Отправить контакт", request_contact=True)

        markup.add(contact)

        bot.send_message(user_id, f'Пожалуйста {d} отправь свой номер начиная с +998',reply_markup=markup)

    # Если user_id есть
    if user_id in user:
            user_id = message.from_user.id

            d = message.from_user.first_name

            kb = types.ReplyKeyboardMarkup(True)

            item = types.KeyboardButton('Заказать')

            kb.add(item)

            bot.send_message(user_id, f'{d} дававй мы продолжим', reply_markup=kb)

    # Иначе
    else:
        bot.send_message(user_id,'Нажмите на кнопку Отправить контакт')
        # bot.register_next_step_handler(message,get_number)


# Обработка контакта
@bot.message_handler(content_types=['contact'])
def contact(message):
    # Если значение при оброботке None
    if message.contact is not None:
        number = message.contact.phone_number

        user_id = message.from_user.id

        d = message.from_user.first_name

        # Функция передачи данных в базу
        data.register(user_id, number, d)

        kb = types.ReplyKeyboardMarkup(True)

        item = types.KeyboardButton('Заказать')

        kb.add(item)

        bot.send_message(user_id, 'Отлично, вы успешно зарегистрировались', reply_markup=kb)


def up_name(id):
    data.update_name(id)


def up_nuber(number):
    data.update_number(number)

# Функция изменения текущего профиля
def dict(message,number):
    user_id = message.from_user.id

    name = message.text

    # Передача данных в функцию
    data.register(user_id,number,name)

    # Получение данных из базы
    user = data.get_uu(message.from_user.id)

    l = 'Теперь твой профиль выглядит вот так:\n\n'

    for i in user:
        prof = f'Ваше имя: {i[2]}\n\nВаш номер: {i[1]}'
        l += prof

    bot.send_message(message.from_user.id, l)

    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)

    item = types.KeyboardButton('Заказать')

    item1 = types.KeyboardButton('Мой профиль')

    markup.add(item, item1)

    bot.send_message(message.from_user.id, 'Что делаем ?', reply_markup=markup)


# Функция для обновления имени в базе
def iiii(message):
    user_id = message.from_user.id

    # Передача данныйх для обновления
    data.update_name(user_id)

    bot.send_message(message.from_user.id, "Отлично теперь отправь мне своё имя", )

    d = message.text

    bot.register_next_step_handler(message,dict,d)


# Функция для удаления корзины
def delete_catr(message):
    data.delet_cart(message.from_user.id)

    bot.send_message(message.from_user.id, 'Ваша корзина пуста')

    kb = types.ReplyKeyboardMarkup(True)

    products = data.get_products()

    for i in products:
        kb.add(i[0])

    cart_kb = types.KeyboardButton('Корзина')

    kb.add(cart_kb)

    bot.send_message(message.from_user.id, 'Выберите товар', reply_markup=kb)

    bot.register_next_step_handler(message, get_about)

# Функция для получения профиля
def profil(message):
    user = data.get_uu(message.from_user.id)

    l = 'Ваш профиль:\n\n'
    for i in user:
        prof = f'Ваше имя: {i[2]}\n\nВаш номер: {i[1]}'

        l += prof

    bot.send_message(message.from_user.id, l)

    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)

    item = types.KeyboardButton('Да')

    item1 = types.KeyboardButton('Нет')

    markup.add(item, item1)

    bot.send_message(message.from_user.id, 'Хотите изменить ?', reply_markup=markup)

# Обработчик текста
@bot.message_handler(content_types=['text'])
def text(message):
    if message.text == 'Назад':
        kb = types.ReplyKeyboardMarkup(True)

        products = data.get_products()

        for i in products:
            kb.add(i[0])

        cart_kb = types.KeyboardButton('Корзина')

        kb.add(cart_kb)

        bot.send_message(message.from_user.id, 'Выберите товар', reply_markup=kb)

        bot.register_next_step_handler(message, get_about)

    if message.text == 'Мой профиль':
        profil(message)

    if message.text == 'Нет':
        kb = types.ReplyKeyboardMarkup(True)

        products = data.get_products()

        for i in products:
            kb.add(i[0])

        cart_kb = types.KeyboardButton('Корзина')

        kb.add(cart_kb)

        bot.send_message(message.from_user.id, 'Выберите товар', reply_markup=kb)

        bot.register_next_step_handler(message, get_about)

    if message.text == 'Отчистить корзину':
        kd  = types.ReplyKeyboardMarkup(True)

        item1 = types.KeyboardButton('Да.')

        item2 = types.KeyboardButton('Нет')

        kd.add(item1,item2)

        bot.send_message(message.from_user.id,'Хотите отчистить корзину ?',reply_markup=kd)

    if message.text == 'Да.':
        delete_catr(message)


    if message.text == 'Да':
        bot.send_message(message.from_user.id, "Хорошо давай изменим твои данные, отправь мне свой номер ", )

        bot.register_next_step_handler(message,iiii)

    if message.text == 'Корзина':
        o = 'Ваша корзина:\n\n'

        user_cart = data.get_cart(message.from_user.id)

        for i in user_cart:
            k = f'{i[1]}: {i[2]} шт.\n'
            o += k

        kd = types.ReplyKeyboardMarkup(True)

        item1 = types.KeyboardButton('Оформить заказ')

        item2 = types.KeyboardButton('Назад')

        item3 = types.KeyboardButton('Отчистить корзину')

        item4 = types.KeyboardButton('Мой профиль')

        kd.add(item1, item2, item3,item4)

        bot.send_message(message.from_user.id, o, reply_markup=kd)
        #
        # bot.register_next_step_handler(message, get_zakaz, o)


    if message.text == 'Заказать':
        kb = types.ReplyKeyboardMarkup(True)

        products = data.get_products()

        for i in products:
            kb.add(i[0])

        cart_kb = types.KeyboardButton('Корзина')

        kb.add(cart_kb)

        bot.send_message(message.from_user.id, 'Выберите товар', reply_markup=kb)

        bot.register_next_step_handler(message, get_about)

    if message.text == 'Нет❌':
        pass

    if message.text == '.Да':
        sennnds(message)

    if message.text == '.Нет':
        o = 'Ваша корзина:\n\n'

        user_cart = data.get_cart(message.from_user.id)

        for i in user_cart:
            k = f'{i[1]}: {i[2]} шт.\n'
            o += k

        kd = types.ReplyKeyboardMarkup(True)

        item1 = types.KeyboardButton('Оформить заказ')

        item2 = types.KeyboardButton('Назад')

        item3 = types.KeyboardButton('Отчистить корзину')

        item4 = types.KeyboardButton('Мой профиль')

        kd.add(item1, item2, item3, item4)

        bot.send_message(message.from_user.id, o, reply_markup=kd)

    if message.text == 'Оформить заказ':
        ws = types.ReplyKeyboardMarkup(True)

        it = types.KeyboardButton('.Да')

        it1 = types.KeyboardButton('.Нет')

        ws.add(it,it1)

        bot.send_message(message.chat.id, 'Хотите оформить заказ ?', reply_markup=ws)





# Функция для подсчёта суммы всех товаров в корзине
def send_users_message(message):
    fun = data.get_fun()

    l = ''

    for i in fun:

        d = i[0]
        for i in d:
            l +=f'{i}'

    print(l)

    bot.send_message(l, 'Привет')


# Функция оформления заказа
def get_zakaz(message):

    if message.text == 'Оформить заказ':
        ws = types.ReplyKeyboardMarkup(True)

        it = types.KeyboardButton('.Да')

        it1 = types.KeyboardButton('.Нет')

        ws.add(it,it1)

        bot.send_message(message.chat.id, 'Хотите оформить заказ ?', reply_markup=ws)

        bot.register_next_step_handler(message,sennnds)


    if message.text == '.Нет':
        o = 'Ваша корзина:\n\n'

        user_cart = data.get_cart(message.from_user.id)

        for i in user_cart:
            k = f'{i[1]}: {i[2]} шт.\n'
            o += k

        kd = types.ReplyKeyboardMarkup(True)

        item1 = types.KeyboardButton('Оформить заказ')

        item2 = types.KeyboardButton('Назад')

        item3 = types.KeyboardButton('Отчистить корзину')

        item4 = types.KeyboardButton('Мой профиль')

        kd.add(item1, item2, item3, item4)

        bot.send_message(message.from_user.id, o, reply_markup=kd)

        bot.register_next_step_handler(message, get_zakaz, o)

    if message.text == 'Назад':
        text(message)

def sennnds(message):
    o = 'Ваша корзина:\n\n'

    user_cart = data.get_cart(message.from_user.id)

    for i in user_cart:
        k = f'{i[1]}: {i[2]} шт.\n'
        o += k

    keyboard = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)

    button_geo = types.KeyboardButton(text="Отправить местоположение", request_location=True)

    # item = types.KeyboardButton('Назад')

    keyboard.add(button_geo)

    bot.send_message(message.chat.id, 'Отправь мне геолокацию', reply_markup=keyboard)

    bot.register_next_step_handler(message, send_zakaz, o)

    bot.register_next_step_handler(message,location)

# Функция отправки заказа
def send_zakaz(message,o):
    gg = data.his_nuber(message.from_user.id)

    num = data.number_get_zakaz()

    p = ''
    for i in gg:
        p += f'Имя клиента: {i[2]}\n\nНомер клиента: {i[1]}'


    l = ''
    for i in num:
        l += f'{i[0]}'



    new_orber = o.replace('Ваша корзина:', 'Ваш заказ:')

    admin_message = o.replace('Ваша корзина:', 'Новый заказ:')


    print(new_orber)

    print(admin_message)

    # Функция добавления номера заказа
    data.number_zakaz()

    bot.send_message(message.from_user.id, f'Заказ успешно оформлен\n\n{new_orber}\n\nЗаказ № {l}')

    bot.send_message(message.from_user.id, f'{admin_message}\n{p}\n\nЗаказ № {l}\n\n\nэто сообщение должно быть отправлено в группу для доставки')

    data.delet_cart(message.from_user.id)



# Функция обработки локации
@bot.message_handler(content_types=["location"])
def location(message):
    if message.location is not None:
        coord = str(message.location.longitude) + ',' + str(message.location.latitude)
        r = requests.get(
            'https://geocode-maps.yandex.ru/1.x/?apikey=' + '4815bbb0-e6e7-4c72-9730-82781ab89fca' + '&format=json&geocode=' + coord)

        if len(r.json()['response']['GeoObjectCollection']['featureMember']) > 0:
            address = r.json()['response']['GeoObjectCollection']['featureMember'][0]['GeoObject'][
                'metaDataProperty'][
                'GeocoderMetaData']['text']

            bot.send_message(message.chat.id, 'Ваш адрес:\n{}'.format(address))

            bot.send_message(message.chat.id, 'Адрес:\n{}'.format(address))

            bot.send_location(message.chat.id, message.location.latitude, message.location.longitude)

            bot.send_message(message.chat.id,'_______________________')

            kb = types.ReplyKeyboardMarkup(True)

            products = data.get_products()

            for i in products:
                kb.add(i[0])

            cart_kb = types.KeyboardButton('Корзина')

            kb.add(cart_kb)

            bot.send_message(message.from_user.id, 'Выберите товар', reply_markup=kb)

            bot.register_next_step_handler(message, get_about)

# Функция выбора количества товара
def get_about(message):
    products = [i[0] for i in data.get_products()]

    if message.text in products:
        user_id = message.from_user.id

        about = [i for i in data.get_about(message.text)]

        # Сохраняю временно в словарь то что выбрал пользователь
        users[user_id] = {}

        users[user_id]['Продукт'] = message.text

        # Создаю кнопки для выбора количества
        count_kb = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=3)

        o = [str(i) for i in range(1, 11)]

        count_kb.add(*o)

        bot.send_photo(user_id,photo=about[0][2] ,caption=f'{about[0][-1]}\nЦена: {about[0][1]}')

        bot.send_message(user_id, f'Выберите количество: ', reply_markup=count_kb)

        #Перехожу на этап выбора количества
        bot.register_next_step_handler(message, add_to_cart)

    else:
        text(message)


# Этап добавления в корзину
def add_to_cart(message):
    quant = message.text

    # Обращаюсь к словарю users куда временно записал название продукта который выбрал пользователь
    product_name = users[message.from_user.id]['Продукт']
    # Добавляю в базу

    data.add_cart(message.from_user.id, product_name, quant)

    bot.send_message(message.from_user.id, 'Товар успешно добавлен в корзину')

    kb = types.ReplyKeyboardMarkup(True)

    products = data.get_products()

    for i in products:
        kb.add(i[0])

    cart_kb = types.KeyboardButton('Корзина')

    kb.add(cart_kb)

    bot.send_message(message.from_user.id, 'Выберите товар', reply_markup=kb)

    bot.register_next_step_handler(message, get_about)


print('bot start')
bot.polling(none_stop=True)
