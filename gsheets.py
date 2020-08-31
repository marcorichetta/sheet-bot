import pickle
import os.path
from typing import List
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
import pandas as pd

from decouple import config

# If modifying these scopes, delete the file token.pickle.
SCOPES = ["https://www.googleapis.com/auth/spreadsheets.readonly"]

# The ID and range of a sample spreadsheet.
SPREADSHEET_ID = config("SPREADSHEET_ID")
RANGE_NAME = "Hoja 1!A60:G"  # De la celda A183 a la G183, para abajo


class GSheets_helper:
    def __init__(self):

        self.creds = None
        # The file token.pickle stores the user's access and refresh tokens, and is
        # created automatically when the authorization flow completes for the first
        # time.
        if os.path.exists("token.pickle"):
            with open("token.pickle", "rb") as token:
                self.creds = pickle.load(token)
        # If there are no (valid) credentials available, let the user log in.
        if not self.creds or not self.creds.valid:
            if self.creds and self.creds.expired and self.creds.refresh_token:
                self.creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    "credentials.json", SCOPES
                )
                self.creds = flow.run_local_server(port=0)
            # Save the credentials for the next run
            with open("token.pickle", "wb") as token:
                pickle.dump(self.creds, token)

    def get_values(self) -> List:
        """ Hacer la conexión con la spreadsheet y obtener los valores del rango solicitado """

        service = build("sheets", "v4", credentials=self.creds)

        # Call the Sheets API
        sheet = service.spreadsheets()
        result = (
            sheet.values().get(spreadsheetId=SPREADSHEET_ID, range=RANGE_NAME).execute()
        )
        values = result.get("values", [])

        return values

    def get_rows(self) -> List:

        values = self.get_values()

        if not values:
            print("Error de lectura de la spreadsheet")

        results: List = []

        for index, row in enumerate(values):
            try:
                if len(row) > 0 and "SEMINARIO DE SISTEMAS" in row[0]:
                    for row in values[index:]:
                        if len(row) == 0:
                            break

                        results.append(row)
            except IndexError:
                break

        return results


if __name__ == "__main__":
    helper = GSheets_helper()

    clases = helper.get_rows()

    print(clases)
