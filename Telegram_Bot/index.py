import telebot
import sqlite3
import datetime as dt


bot = telebot.TeleBot('6260341046:AAEon6fpsK_hiq67oIafCmJWJ6NSw9U3GOc')
con = sqlite3.connect('../db/users1.db')


@bot.message_handler(commands=['start'])
def start(message):
    time = dt.datetime.now().strftime('%H')
    if int(time) > 16:
        bot.send_message(chat_id=message.chat.id,
                         text='Добрый вечер, спасибо за регистарцию на сайте! \n'
                              'Для доп. информаци напишите /help')
    elif 4 < int(time) < 11:
        bot.send_message(chat_id=message.chat.id,
                         text='Доброе утро, спасибо за регистарцию на сайте! \n'
                              'Для доп. информаци напишите /help')
    else:
        bot.send_message(chat_id=message.chat.id,
                         text='Добрый день, спасибо за регистарцию на сайте! \n'
                              'Для доп. информаци напишите /help')


@bot.message_handler(commands=['help'])
def help(message):
    bot.send_message(chat_id=message.chat.id, text='Для того чтобы законектить сайт и бота, '
                                                   'напишите /link ваш token с сайта ')


@bot.message_handler(commands=['link'])
def link(message):
    token = message.text.split()
    if token[-1] == '/link':
        bot.send_message(chat_id=message.chat.id, text='Вы не ввели токен')
    else:
        async with con.execute(f""" SELECT login FROM users WHERE bot_id = '{token[-1]}' """) as cr:
            res = await cr.fetchone()
        if res is None:
            bot.send_message(chat_id=message.chat.id,
                             text='Похоже вы ошиблись в токене! Попробуйте снова')
        else:
            bot.send_message(chat_id=message.chat.id, text='Все прошло успешно!')
        print(res)


bot.polling(none_stop=True)
