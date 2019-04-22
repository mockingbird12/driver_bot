import config
import telebot
import markup
from dbdriver import UserStatus, Loaders
from telebot import types
from telebot import apihelper

bot = telebot.TeleBot(config.token)
user = UserStatus()
loader_dict = {}

@bot.message_handler(commands=['admin'])
def admin(message):
    ans = 'Redirect to admin'
    markup = admin()
    bot.send_message(message.chat.id, ans, reply_markup=markup)

@bot.message_handler(func=lambda message: message.text == 'Удалить анкету')
def delete_user(message):
    user.user_id = message.chat.id
    user.delete_user()
    loader = Loaders()
    loader.delete(message.chat.id)
    bot.send_message(message.chat.id, 'Ваша анкета удалена')

@bot.message_handler(func=lambda message: message.text == 'Проверить статус')
def reset(message):
    markup_key = markup.broken_registration()
    if user.get_status(message.chat.id) != config.END_REGISTRATION:
        bot.send_message(message.chat.id, 'Регистрация не завершена, либо пройдена некорректно', reply_markup=markup_key)
    else:
        loader = Loaders()
        if loader.check_exsist(message.chat.id):
            if loader.get_accept_status(message.chat.id) == config.ACCEPT:
                bot.send_message(message.chat.id, 'Заявка одобрена')
            if loader.get_accept_status(message.chat.id) == config.DECLAIN:
                bot.send_message(message.chat.id, 'Заявка отклонена')
            if loader.get_accept_status(message.chat.id) == config.WAITING:
                bot.send_message(message.chat.id, 'Заявка не просмотрена')
        else:
            bot.send_message(message.chat.id, 'Данного пользователя не существует',
                             reply_markup=markup_key)


@bot.message_handler(func=lambda message: message.text == 'Заново')
def reset(message):
    loader_dict = {}
    user.user_id = message.chat.id
    user.set_status(config.START)
    bot.send_message(message.chat.id, 'Начинаем регистрацию заново')
    chose_special(message)

@bot.message_handler(commands=['start'])
def workers(message):
    user.user_id = str(message.chat.id)
    user.set_status(config.START)
    markup_key = markup.workers_markup()
    bot.send_message(message.chat.id, 'hi', reply_markup=markup_key)

@bot.message_handler(func=lambda message: user.get_status(message.chat.id) == config.END_REGISTRATION)
def waiting_accept(message):
    bot.send_message(message.chat.id, 'Пользователь существует, ждите ответа')

@bot.message_handler(content_types=["photo", "text"], func=lambda message: user.get_status(message.chat.id) == config.LAST_STEP)
def end_registration(message):
    print(loader_dict)
    user.user_id = message.chat.id
    if message.photo == None:
        bot.send_message(message.chat.id, 'Отправьте фото')
        return False
    photo = message.photo[-1].file_id
    print('Person foto - ' + photo)
    loader_dict.update({'person_foto':photo})
    loader = Loaders()
    if not loader.check_exsist(user.user_id):
        markup_key = markup.main_menu()
        loader.insert_data(user.user_id, loader_dict)
        bot.send_message(message.chat.id, 'Регистрация завершена. Ваша заявка обрабатывается.', reply_markup=markup_key)
        user.set_status(config.END_REGISTRATION)
    else:
        markup_keyboard = markup.workers_markup()
        bot.send_message(message.chat.id, 'Такой пользователь уже существует.', reply_markup=markup_keyboard)

@bot.message_handler(content_types=["photo", "text"], func=lambda message: user.get_status(message.chat.id) == config.ENTER_PASSPORT_FOTO)
def person_foto(message):
    keyboard = markup.reset()
    user.user_id = str(message.chat.id)
    if message.photo == None:
        bot.send_message(message.chat.id, 'Отправьте фото паспорта', reply_markup=keyboard)
        return False
    photo = message.photo[-1].file_id
    print('Passport foto - '+ photo)
    loader_dict.update({'passport_foto': photo})
    bot.send_message(message.chat.id, 'Отправьте фото', reply_markup=keyboard)
    user.set_status(config.LAST_STEP)

@bot.message_handler(func=lambda message: user.get_status(message.chat.id) == config.ENTER_DISTRICT)
def passport_foto(message):
    keyboard = markup.reset()
    user.user_id = str(message.chat.id)
    district = message.text
    print('District - '+district)
    loader_dict.update({'district': district})
    bot.send_message(message.chat.id, 'Отправьте фото паспорта', reply_markup=keyboard)
    user.set_status(config.ENTER_PASSPORT_FOTO)

@bot.message_handler(func=lambda message: user.get_status(message.chat.id) == config.ENTER_FIO)
def choose_district(message):
    fio = message.text
    print('Fio - ' + fio)
    loader_dict.update({'fio': fio})
    markup_key = markup.reset()
    bot.send_message(message.chat.id, 'Выберите ваш район', reply_markup=markup_key)
    user.set_status(config.ENTER_DISTRICT)


@bot.message_handler(func=lambda message: user.get_status(message.chat.id) == config.ENTER_SPEC)
def enter_fio(message):
    user.user_id = message.chat.id
    keyboard_hider = types.ReplyKeyboardRemove()
    spec = message.text
    print('Spec - ' + spec)
    loader_dict.update({'spec':spec})
    bot.send_message(message.chat.id, 'Введите ФИО', reply_markup=keyboard_hider)
    user.set_status(config.ENTER_FIO)
    pass

@bot.message_handler(func=lambda message: user.get_status(message.chat.id) == config.START)
def chose_special(message):
    markup_key = markup.special()
    bot.send_message(message.chat.id, 'Выберите профессию', reply_markup=markup_key)
    user.set_status(config.ENTER_SPEC)


@bot.message_handler(content_types=['text'])
def repeat(message):
    user.user_id = str(message.chat.id)
    keyboard_hider = types.ReplyKeyboardRemove()
    if user.get_status(message.chat.id):
        print('User exsist')
        markup_key = markup.main_menu()
        bot.send_message(message.chat.id, 'Пользователь существует, чтобы зарегистрироваться вы должны удалить анкету',
                         reply_markup=markup_key)
        return False
    if message.text == 'Просмотр анкет':
        bot.send_message(message.chat.id, 'Просмотр анкет', reply_markup=keyboard_hider)
    if message.text == 'Проверить статус':
        bot.send_message(message.chat.id, 'Проверить статус', reply_markup=keyboard_hider)
    if message.text == 'Зарегистрироваться':
        print('status - '+ str(config.START))
        user.set_status(config.START)
        chose_special(message)
    if message.text == 'Удалить анкету':
        bot.send_message(message.chat.id, 'Удалить анкету', reply_markup=keyboard_hider)
        user.delete_user()
        print('Delete from table')
    else:
        bot.send_message(message.chat.id, 'Usage')


if __name__=='__main__':
    print('Starting bot')
    # apihelper.proxy = { 'https': 'socks5://127.0.0.1:9050'}
    bot.polling()