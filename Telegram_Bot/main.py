from telegram.ext import CommandHandler, Application
import datetime as dt
from requests import get, put


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
                                        'напишите /linking_to_a_bot и ваш token с сайта \n'
                                        'Для того чтобы проверить самую близжайшую задачу,'
                                        'напишите /check_tasks и ваш id')


async def linking_to_a_bot(update, context):
    token = update.message.text.split()
    if token[-1] == '/linking_to_a_bot':
        await context.bot.send_message(chat_id=update.effective_chat.id, text='Вы не ввели токен!')
    else:
        res = get(f'https://octagonal-thankful-operation.glitch.me/check_link/{token[-1]}')
        if res:
            put(f'https://octagonal-thankful-operation.glitch.me/link/{token[-1]}')
            await context.bot.send_message(chat_id=update.effective_chat.id,
                                           text='Удачно!')
        if res is None:
            await context.bot.send_message(chat_id=update.effective_chat.id,
                                           text='Похоже вы ошиблись в токене! Попробуйте снова')


async def check_tasks(update, context):
    id = update.message.text.split()[-1]
    if id.isdigit() and id:
        res = get(f'https://octagonal-thankful-operation.glitch.me/check_task/{int(id)}').json()
        if res is None:
            await context.bot.send_message(chat_id=update.effective_chat.id,
                                           text='У вас нету поставленных задач')
        else:
            if res['tasks']:
                arr = []
                for el in res['tasks']:
                    arr.append(el['created_date'])
                await context.bot.send_message(chat_id=update.effective_chat.id,
                                               text=f'До близжайшей задачи вам осталось: '
                                                    f'{min(arr)}')
            else:
                await context.bot.send_message(chat_id=update.effective_chat.id,
                                               text='У вас еще нету поставленных задач!')
    else:
        await context.bot.send_message(chat_id=update.effective_chat.id,
                                       text='Вы не ввели id или ошиблись при наборе id')


async def send_message(update, context):
    args = context.args
    message = ' '.join(args)
    await context.bot.send_message(chat_id=update.effective_chat.id, text=message)


async def error(update, context):
    print(f'caused error {context.error}')


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
