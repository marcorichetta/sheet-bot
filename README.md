# Sh(ee)t Bot

-   Lee un rango de celdas de un spreadsheet
-   Formatea los datos y me manda un mensaje con cada clase por Telegram

### Requisitos

1. Habilitar [Google Sheets API](https://developers.google.com/sheets/api/quickstart/python#step_1_turn_on_the)

    - Esto te permite hacer peticiones a la API de Sheets
    - Descargar el archivo `credentials.json` (:warning: No compartas este archivo)
    - Ubicarlo en la raíz de este directorio junto a `gsheets.py` y `telegram_bot.py`

2. [Crear tu bot de Telegram](https://core.telegram.org/bots#6-botfather)

3. Renombrar el archivo `.env.template` => `.env` (:warning: No compartas este archivo)

4. Completar con tu token y el ID de la spreadsheet (Asegurate de poder acceder con tu usuario de Google o de que sea pública)

```bash
git clone https://github.com/marcorichetta/sheet-bot.git

# Crear virtualenv (Recomendado)
python3 -m venv env

# Activar virtualenv
source env/bin/activate

# Instalar dependencias
pip install -r requirements.txt

# Ejecutar el bot
python telegram_bot.py
```
