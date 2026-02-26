import os
from google.oauth2.service_account import Credentials
import gspread

def get_sheets_client():
    """
    Authenticates with Google Sheets using a service account JSON file.
    The file should be named 'credentials.json' and placed in the project root.
    """
    scopes = [
        "https://www.googleapis.com/auth/spreadsheets",
        "https://www.googleapis.com/auth/drive"
    ]
    
    cred_path = "credentials.json"
    
    if not os.path.exists(cred_path):
        print(f"Warning: {cred_path} not found. Sheets integration disabled.")
        return None
        
    try:
        credentials = Credentials.from_service_account_file(cred_path, scopes=scopes)
        client = gspread.authorize(credentials)
        return client
    except Exception as e:
        print(f"Error authenticating with Google Sheets: {e}")
        return None

def log_lead(name: str, phone: str, message: str, is_serious: bool = True, date: str | None = None):
    """
    Appends a new row to the configured Google Sheet.
    """
    sheet_url = os.getenv("GOOGLE_SHEET_URL")
    if not sheet_url:
        print("GOOGLE_SHEET_URL missing in .env")
        return False
        
    client = get_sheets_client()
    if not client:
        return False
        
    try:
        # Open by URL and get the first worksheet
        sheet = client.open_by_url(sheet_url).sheet1
        
        from datetime import datetime
        if not date:
            date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            
        serious_str = "Yes" if is_serious else "No"
        
        # Append [Date, Name, Phone, Message, Is Serious?, Status]
        row = [date, name, phone, message, serious_str, "Pending Reply"]
        sheet.append_row(row)
        
        print("Lead logged to Google Sheets successfully.")
        return True
    except Exception as e:
        print(f"Error logging to Google Sheets: {e}")
        return False
