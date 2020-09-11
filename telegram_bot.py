import os, time, logging
from typing import List
from decouple import config
from telegram.ext import CallbackContext, CommandHandler, Updater
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
    time.sleep(1)

    update.message.reply_text("🤖 Hola humano!")

    mensaje = """
🕹 *Instrucciones*

/clases - Obtener las clases que hayan sido agregadas
/recordatorio - Configurar envío de mensajes cada 3 hs
"""

    update.message.reply_markdown(mensaje)


def clases(context: CallbackContext):
    """ Envía un mensaje por cada nueva clase """

    job = context.job

    context.bot.send_message(job.context, text="Veamos si hay nuevas clases")

    time.sleep(2)

    # Buscar las clases en Sheets
    items = helper.get_rows()

    # Excluir las filas con datos innecesarios (Primeras 2)
    clases = items[2:]

    # Leer la constante (Cantidad de clases registradas por el boy)
    with open("clases.txt", "r") as file:
        num_clases_viejas = file.read()

    num_clases_viejas = int(num_clases_viejas)

    if len(clases) == num_clases_viejas:
        context.bot.send_message(job.context, text="Nada nuevo mugroso perro 🧔🏼")
        return

    # Se encontraron nuevas clases
    context.bot.send_message(job.context, text="Tome sus mugrosas clases Richetta 🧔🏼")

    # Para separar las nuevas clases recorremos la lista
    # a partir del índice, que corresponde al num de clases anterior
    clases_nuevas: List[str] = clases[num_clases_viejas:]

    for clase in clases_nuevas:
        mensaje = formatear(clase)
        time.sleep(2)
        context.bot.send_message(job.context, text=mensaje)

    # Guardamos el nuevo num de clases
    with open("clases.txt", "w") as file:
        nuevo_num = str(len(clases))
        file.write(nuevo_num)

    time.sleep(2)

    context.bot.send_message(job.context, text="Eso es todo mugroso estudiante 🧔🏼")

def recordatorio(update, context: CallbackContext):
    """ Configurar el recordatorio para correr `clases()` cada 6 hs """

    chat_id = update.message.chat_id

    new_job = context.job_queue.run_repeating(callback=clases, interval=21600, context=chat_id) 
    context.chat_data['job'] = new_job

    update.message.reply_text("Se configuró el recordatorio!")

def main():
    """ Correr el bot """
    updater = Updater(token=TOKEN, use_context=True)

    # Get the dispatcher to register handlers
    dispatcher = updater.dispatcher

    start_handler = CommandHandler("start", start)
    clases_handler = CommandHandler("clases", clases)
    recordatorio_handler = CommandHandler("recordatorio", recordatorio)

    dispatcher.add_handler(start_handler)
    dispatcher.add_handler(clases_handler)
    dispatcher.add_handler(recordatorio_handler)


    updater.start_polling()
    print("Arrancó")

    updater.idle()


if __name__ == "__main__":
    main()
