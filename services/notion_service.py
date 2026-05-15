import os
import requests
from utils.config import Config

class NotionService:
    def __init__(self):
        self.api_key = Config.NOTION_API_KEY
        self.headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
            "Notion-Version": "2022-06-28"
        }
        
    def export_summary(self, database_id, total_income, total_expense, balance):
        """
        Mock function to demonstrate Notion integration.
        In a real scenario, this would POST data to the Notion API.
        """
        if not self.api_key or self.api_key == 'your_notion_api_key_here':
            print("Notion API key not configured. Skipping export.")
            return False
            
        print(f"Exporting to Notion DB: {database_id}")
        
        # Example payload structure for Notion
        payload = {
            "parent": { "database_id": database_id },
            "properties": {
                "Title": { "title": [{"text": {"content": "Monthly Summary"}}] },
                "Income": { "number": total_income },
                "Expenses": { "number": total_expense },
                "Balance": { "number": balance }
            }
        }
        
        # In a real app:
        # response = requests.post("https://api.notion.com/v1/pages", json=payload, headers=self.headers)
        # return response.status_code == 200
        
        return True
