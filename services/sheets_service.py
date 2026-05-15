import os
import gspread
from google.oauth2.service_account import Credentials
from utils.config import Config

class GoogleSheetsService:
    def __init__(self):
        self.credentials_path = Config.GOOGLE_SHEETS_CREDENTIALS
        
    def append_row(self, sheet_id, data_list):
        """
        Appends a row to a Google Sheet using the gspread library.
        """
        if not self.credentials_path or self.credentials_path == 'your_google_sheets_credentials_json_here' or not os.path.exists(self.credentials_path):
            print("Google Sheets credentials not configured or file not found. Skipping export.")
            return False
            
        if not sheet_id or sheet_id == 'your_target_google_sheet_id_here':
            print("Target Google Sheet ID not configured. Skipping export.")
            return False

        print(f"Appending row to Google Sheet {sheet_id}: {data_list}")
        
        try:
            scopes = [
                'https://www.googleapis.com/auth/spreadsheets',
                'https://www.googleapis.com/auth/drive'
            ]
            creds = Credentials.from_service_account_file(self.credentials_path, scopes=scopes)
            client = gspread.authorize(creds)
            
            sheet = client.open_by_key(sheet_id).sheet1
            sheet.append_row(data_list)
            return True
        except Exception as e:
            print(f"Failed to append row to Google Sheets: {e}")
            return False
