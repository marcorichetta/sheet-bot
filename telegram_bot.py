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
    update.message.reply_text(
        "Usa /clases para obtener las clases que hayan sido agregadas"
    )


def clases(update, context):
    """ Envía un mensaje por cada nueva clase """

    update.message.reply_text("Veamos si hay nuevas clases")

    items = helper.get_rows()

    # Excluir las filas con datos innecesarios (Primeras 2)
    clases = items[2:]

    # Leer la constante
    with open("clases.txt", "r") as file:
        num_clases_viejas = file.read()

    num_clases_viejas = int(num_clases_viejas)

    if len(clases) == num_clases_viejas:
        update.message.reply_text("Nada nuevo perro 🧔🏼")
        return

    update.message.reply_text("Tome sus mugrosas clases Richetta 🧔🏼")
    
    # Para separar las nuevas clases recorremos la lista
    # a partir del índice, que corresponde al num de clases anterior
    clases_nuevas: List[str] = clases[num_clases_viejas:]

    for clase in clases_nuevas:
        mensaje = formatear(clase)
        time.sleep(1)
        update.message.reply_text(mensaje)

    # Guardamos el nuevo num de clases
    with open("clases.txt", "w") as file:
        nuevo_num = str(len(clases))
        file.write(nuevo_num)

    time.sleep(1)
    update.message.reply_text("Eso es todo mugroso estudiante 🧔🏼")


def timer():
    # https://github.com/python-telegram-bot/python-telegram-bot/blob/master/examples/timerbot.py
    pass


def main():
    """ Correr el bot """
    updater = Updater(token=TOKEN, use_context=True)

    # Get the dispatcher to register handlers
    dispatcher = updater.dispatcher

    start_handler = CommandHandler("start", start)
    clases_handler = CommandHandler("clases", clases)

    dispatcher.add_handler(start_handler)
    dispatcher.add_handler(clases_handler)

    updater.start_polling()
    print("Arrancó")

    updater.idle()


if __name__ == "__main__":
    main()
