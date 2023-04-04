from telegram.ext import CommandHandler, Application
import datetime as dt


async def start(update, context):
    time = dt.datetime.now().strftime('%H')
    if int(time) > 16:
        await context.bot.send_message(chat_id=update.effective_chat.id,
                                       text='Добрый вечер, спасибо за регистарцию на сайте!')
    elif 4 < int(time) < 11:
        await context.bot.send_message(chat_id=update.effective_chat.id,
                                       text='Доброе утро, спасибо за регистарцию на сайте!')
    else:
        await context.bot.send_message(chat_id=update.effective_chat.id,
                                       text='Добрый день, спасибо за регистарцию на сайте!')


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
    app.add_error_handler(error)
    app.run_polling()


if __name__ == '__main__':
    main()
