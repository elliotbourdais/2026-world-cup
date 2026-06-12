import requests
import pandas as pd
import gspread
import json
import os
from google.oauth2.service_account import Credentials

SHEET_NAME = "2026 World Cup"
TAB_NAME = "Automated Results"

# Load credentials from GitHub secret
creds_json = json.loads(os.environ["GOOGLE_CREDENTIALS"])
scopes = ["https://www.googleapis.com/auth/spreadsheets",
          "https://www.googleapis.com/auth/drive"]
creds = Credentials.from_service_account_info(creds_json, scopes=scopes)
client = gspread.authorize(creds)

# Fetch data
url = "https://raw.githubusercontent.com/upbound-web/worldcup-live.json/master/2026/worldcup.json"
data = requests.get(url).json()
df = pd.DataFrame(data['matches']).fillna('')

# Write to Google Sheets
sheet = client.open(SHEET_NAME).worksheet(TAB_NAME)
sheet.clear()
sheet.update([df.columns.tolist()] + df.values.tolist())

print("Results updated successfully")
