import os
import requests
from utils.config import Config

class GoogleSheetsService:
    def __init__(self):
        self.webhook_url = Config.GOOGLE_SHEET_WEBHOOK_URL
        
    def append_row(self, webhook_url, data_list):
        """
        Appends a row to a Google Sheet using a Google Apps Script Webhook.
        """
        url = webhook_url or self.webhook_url
        if not url or url == 'your_google_sheet_webhook_url_here':
            print("Google Sheet Webhook URL not configured. Skipping export.")
            return False

        print(f"Sending row to Google Sheet Webhook: {data_list}")
        
        try:
            # data_list is expected to be [month, income, expense, balance]
            payload = {
                "month": data_list[0],
                "income": data_list[1],
                "expense": data_list[2],
                "balance": data_list[3]
            }
            response = requests.post(url, json=payload)
            response.raise_for_status()
            print("Webhook Response:", response.text)
            return True
        except Exception as e:
            print(f"Failed to append row via Webhook: {e}")
            return False
