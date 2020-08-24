from telegram.ext import CommandHandler, Filters, MessageHandler, Updater

from conf.settings import BASE_API_URL, TELEGRAM_TOKEN

import logging

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', 
    level=logging.INFO
)


def start(update, context):
    response_message = "=^._.^="
    context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=response_message
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
    response_message = "Meow? =^._.^="
    context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=response_message
    )


def echo(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text=update.message.text)


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
