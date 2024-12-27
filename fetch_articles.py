import os
import json
import gspread
from google.oauth2.service_account import Credentials
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Hardcoded variables
SPREADSHEET_ID = '1z0tPzic-a_hPtadZufK2ndEbij7NYP7m8EmZQwXGld4'
RANGE_NAME = 'All Prompts'
CREDENTIALS_FILE = os.getenv("GOOGLE_CREDENTIALS_FILE")

def fetch_articles(spreadsheet_id, range_name):
    # Set up the Sheets API
    scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
    creds = Credentials.from_service_account_file(CREDENTIALS_FILE, scopes=scope)
    client = gspread.authorize(creds)

    # Fetch the data
    try:
        sheet = client.open_by_key(spreadsheet_id).worksheet(range_name)
        articles = sheet.get_all_records()
        print(f"Fetched {len(articles)} articles")
        for article in articles:
            print(article)
        return articles
    except gspread.exceptions.WorksheetNotFound:
        print(f"Worksheet with name '{range_name}' not found in spreadsheet '{spreadsheet_id}'.")
        print("Available worksheets:")
        spreadsheet = client.open_by_key(spreadsheet_id)
        for worksheet in spreadsheet.worksheets():
            print(worksheet.title)
        raise

if __name__ == "__main__":
    articles = fetch_articles(SPREADSHEET_ID, RANGE_NAME)
    print(articles)