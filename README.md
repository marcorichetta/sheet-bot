# Sh(ee)t Bot

-   Lee un rango de celdas de un spreadsheet
-   Formatea los datos y me manda un mensaje con cada clase por Telegram

### Requisitos

1. Habilitar [Google Sheets API](https://developers.google.com/sheets/api/quickstart/python#step_1_turn_on_the)

    - Esto te permite hacer peticiones a la API de Sheets
    - Descargar el archivo `credentials.json` y ubicarlo en la raíz de este directorio

2. [Crea tu bot de Telegram](https://core.telegram.org/bots#6-botfather)

```bash
python3 -m venv env

source env/bin/activate

pip install -r requirements.txt

TELEGRAM_TOKEN => Token de Telegram para tu bot
SPREADSHEET_ID => Id del spreadsheet al que querés acceder

python telegram_bot.py
```
