import requests
import gspread
import json
import os
from collections import defaultdict
from google.oauth2.service_account import Credentials

SHEET_NAME = "2026 World Cup"
TAB_NAME = "Stats"

# Load credentials from GitHub secret
creds_json = json.loads(os.environ["GOOGLE_CREDENTIALS"])
scopes = ["https://www.googleapis.com/auth/spreadsheets",
          "https://www.googleapis.com/auth/drive"]
creds = Credentials.from_service_account_info(creds_json, scopes=scopes)
client = gspread.authorize(creds)

# Fetch data
url = "https://raw.githubusercontent.com/upbound-web/worldcup-live.json/master/2026/worldcup.json"
data = requests.get(url).json()

# Count goals
goal_counts = defaultdict(int)
for match in data['matches']:
    for col in ['goals1', 'goals2']:
        for goal in match.get(col, []):
            if not goal.get('owngoal', False):
                goal_counts[goal['name']] += 1

top_scorers = sorted(goal_counts.items(), key=lambda x: x[1], reverse=True)

# Write to Google Sheets
sheet = client.open(SHEET_NAME).worksheet(TAB_NAME)
sheet.clear()
sheet.update([['Player', 'Goals']] + [list(row) for row in top_scorers])

print("Goalscorers updated successfully")
