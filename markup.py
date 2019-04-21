from telebot import types

def admin():
    markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
    admin_keys = ['Просмотр анкет']
    for item in admin_keys: markup.add(item)
    return markup

def broken_registration():
    markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
    items = ['Удалить анкету', 'Заново']
    for item in items: markup.add(item)
    return markup

def workers_markup():
    markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
    items = ['Проверить статус', 'Зарегистрироваться', 'Удалить анкету', 'Заново']
    for item in items: markup.add(item)
    return markup

def special():
    markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
    items = ['Водитель', 'Грузчик']
    for item in items: markup.add(item)
    return markup

def district():
    markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
    items = ['Дзержинский', 'Центральный']
    for item in items: markup.add(item)
    return markup

def main_menu():
    markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
    items = ['Проверить статус', 'Зарегистрироваться', 'Удалить анкету']
    for item in items: markup.add(item)
    return markup