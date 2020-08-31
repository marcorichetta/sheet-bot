import logging
import os
import time
from typing import List

from telegram.ext import CommandHandler, Updater
from decouple import config

from gsheets import GSheets_helper

helper = GSheets_helper()

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)

logger = logging.getLogger(__name__)

TOKEN = config("TELEGRAM_TOKEN")


def formatear(clase: List) -> str:
    """
        ['25/08/2020',
        '20:00 / --:--',
        'Normal',
        'En directo',
        'URL',
        '<',
        'Observaciones']
    """
    try:
        obs = clase[6]
    except IndexError:
        obs = "No hay observaciones"

    return f"""
    Fecha: {clase[0]}
    Hora: {clase[1]}
    Observaciones: {obs}
    Link: {clase[4]}
    """


# Define a few command handlers. These usually take the two arguments update and
# context. Error handlers also receive the raised TelegramError object in error.
def start(update, context):
    """Send a message when the command /start is issued."""
    update.message.reply_text("Hola humano")
    update.message.reply_text("Toma tus mugrosas clases")

    items = helper.get_rows()

    # Excluir las filas con datos innecesarios
    clases = items[2:]

    for clase in clases:
        mensaje = formatear(clase)
        time.sleep(1)
        update.message.reply_text(mensaje)


def timer():
    # https://github.com/python-telegram-bot/python-telegram-bot/blob/master/examples/timerbot.py
    pass


def main():
    """ Correr el bot """
    updater = Updater(token=TOKEN, use_context=True)

    # Get the dispatcher to register handlers
    dispatcher = updater.dispatcher

    start_handler = CommandHandler("start", start)

    dispatcher.add_handler(start_handler)

    updater.start_polling()
    print("Arrancó")

    updater.idle()


if __name__ == "__main__":
    main()
