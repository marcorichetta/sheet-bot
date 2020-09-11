# Sh(ee)t Bot

-   Lee un rango de celdas de un spreadsheet
-   Formatea los datos y me manda un mensaje con cada clase por Telegram

### Requisitos

1. Habilitar [Google Sheets API](https://developers.google.com/sheets/api/quickstart/python#step_1_turn_on_the)

    - Esto te permite hacer peticiones a la API de Sheets
    - Descargar el archivo `credentials.json` (:warning: No compartas este archivo)
    - Ubicarlo en la raíz de este directorio junto a `gsheets.py` y `telegram_bot.py`

2. `git clone https://github.com/marcorichetta/sheet-bot.git`

3. [Crear tu bot de Telegram](https://core.telegram.org/bots#6-botfather)

4. Renombrar el archivo `.env.template` => `.env` (:warning: No compartas este archivo)

5. Completar con tu token y el ID de la spreadsheet (Asegurate de poder acceder con tu usuario de Google o de que sea pública)

```bash
# Crear virtualenv (Recomendado)
python3 -m venv env

# Activar virtualenv
source env/bin/activate

# Instalar dependencias
pip install -r requirements.txt

# Ejecutar el bot
python telegram_bot.py
```

### Autorización

La primera vez que se ejecuta el bot se te pedirá que ingreses a un link para autorizar a tu app.

```bash
Please visit this URL to authorize this application: https://accounts.google.com/o/oauth2/auth?response_type=...
```

Una vez completada la autorización de Google, se creará un archivo [`token.pickle`](https://docs.python.org/3/library/pickle.html), el cual contiene los tokens de acceso para leer la spreadsheet.
