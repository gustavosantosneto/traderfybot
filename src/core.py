from telegram.ext import CommandHandler, Filters, MessageHandler, Updater

from conf.settings import BASE_API_URL, TELEGRAM_TOKEN

import logging
import schedule
import time

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    # level=logging.INFO
)

my_chat_id = ''
context = ''
started = False


async def init(update, _context):
    global started

    if not started:
        print('init')
        global my_chat_id
        global context

    my_chat_id = update.effective_chat.id
    context = _context

    schedule.every(10).seconds.do(checkTrigger)

    await run_schedule()

    started = True


async def run_schedule():
    while True:
        schedule.run_pending()
        time.sleep(1)


def start(update, context):

    if not started:
        init(update, context)

    response_message = "<b>=^._.^=</b>"

    context.bot.send_message(
        chat_id=my_chat_id,
        text=response_message,
        parse_mode="html"
    )


def checkTrigger():
    print('checkTrigger')
    context.bot.send_message(
        chat_id=my_chat_id,
        text="10 seconds message",
        parse_mode='html'
    )


def http_cats(update, context):
    if context.args:
        context.bot.sendPhoto(
            chat_id=update.effective_chat.id,
            photo=BASE_API_URL + context.args[0]
        )
    else:
        context.bot.sendPhoto(
            chat_id=update.effective_chat.id,
            photo=BASE_API_URL + "100"
        )


def unknown(update, context):
    if not started:
        init(update, context)

    response_message = "Meow? =^._.^="
    context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=response_message
    )


def echo(update, context):
    if not started:
        init(update, context)

    context.bot.send_message(
        chat_id=update.effective_chat.id, text=update.message.text)


def main():
    updater = Updater(token=TELEGRAM_TOKEN, use_context=True)

    dispatcher = updater.dispatcher

    dispatcher.add_handler(
        CommandHandler('start', start)
    )
    dispatcher.add_handler(
        CommandHandler('http', http_cats, pass_args=True)
    )
    dispatcher.add_handler(
        MessageHandler(Filters.command, unknown)
    )
    dispatcher.add_handler(
        MessageHandler(Filters.text & (~Filters.command), echo)
    )

    updater.start_polling()

    updater.idle()


if __name__ == '__main__':
    print("press CTRL + C to cancel.")
    main()
