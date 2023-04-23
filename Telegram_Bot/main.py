from telegram.ext import CommandHandler, Application
import datetime as dt
import aiosqlite
from requests import get


async def start(update, context):
    time = dt.datetime.now().strftime('%H')
    if int(time) > 16:
        await context.bot.send_message(chat_id=update.effective_chat.id,
                                       text='Добрый вечер, спасибо за регистарцию на сайте! \n'
                                            'Для доп. информаци напишите /help')
    elif 4 < int(time) < 11:
        await context.bot.send_message(chat_id=update.effective_chat.id,
                                       text='Доброе утро, спасибо за регистарцию на сайте! \n'
                                            'Для доп. информаци напишите /help')
    else:
        await context.bot.send_message(chat_id=update.effective_chat.id,
                                       text='Добрый день, спасибо за регистарцию на сайте! \n'
                                            'Для доп. информаци напишите /help')


async def help(update, context):
    await context.bot.send_message(chat_id=update.effective_chat.id,
                                   text='Для того чтобы законектить сайт и бота, '
                                        'напишите /linking_to_a_bot и ваш token с сайта')


async def linking_to_a_bot(update, context):
    token = update.message.text.split()
    if token[-1] == '/linking_to_a_bot':
        await context.bot.send_message(chat_id=update.effective_chat.id, text='Вы не ввели токен!')
    else:
        async with aiosqlite.connect('../db/users1.db') as conn:
            async with conn.execute(f'SELECT login FROM users WHERE bot_id = "{token[-1]}" ') \
                    as cursor:
                res = await cursor.fetchone()

        if res is None:
            await context.bot.send_message(chat_id=update.effective_chat.id,
                                           text='Похоже вы ошиблись в токене! Попробуйте снова')
        else:
            await context.bot.send_message(chat_id=update.effective_chat.id,
                                           text=f'Приятно познакомиться, {res[0][0]}')


async def check_tasks(update, context):
    id = update.message.text.split()[-1]
    if id.isdigit() and id:
        res = get(f'http://localhost:5000/check_task/{int(id)}')
        print(res)
        if res is None:
            await context.bot.send_message(chat_id=update.effective_chat.id,
                                           text='У вас нету поставленных задач')
        else:
            arr = []
            for el in res:
                arr.append(el.created_date)
            await context.bot.send_message(chat_id=update.effective_chat.id,
                                           text=f'До близжайшей задачи вам осталось: {min(arr)}')
    else:
        await context.bot.send_message(chat_id=update.effective_chat.id,
                                       text='Вы не ввели id или ошиблись при наборе id')


async def send_message(update, context):
    args = context.args
    message = ' '.join(args)
    await context.bot.send_message(chat_id=update.effective_chat.id, text=message)


async def error(update, context):
    print(f'Update {update} caused error {context.error}')


def main():
    app = Application.builder().token('6260341046:AAEon6fpsK_hiq67oIafCmJWJ6NSw9U3GOc').build()
    app.add_handler(CommandHandler('start', start))
    app.add_handler(CommandHandler('send', send_message))
    app.add_handler(CommandHandler('linking_to_a_bot', linking_to_a_bot))
    app.add_handler(CommandHandler('help', help))
    app.add_handler(CommandHandler('check_tasks', check_tasks))
    app.add_error_handler(error)
    app.run_polling()


if __name__ == '__main__':
    main()
