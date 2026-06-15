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

TEAM_NAME_FIX = {
    "USA": "United States",
    "Bosnia & Herzegovina": "Bosnia and Herzegovina",
}

COUNTRY_CODE = {
    "Mexico": "mx",
    "South Korea": "kr",
    "Canada": "ca",
    "United States": "us",
    "Qatar": "qa",
    "Brazil": "br",
    "Haiti": "ht",
    "Australia": "au",
    "Germany": "de",
    "Netherlands": "nl",
    "Ivory Coast": "ci",
    "Sweden": "se",
    "Spain": "es",
    "Belgium": "be",
    "Saudi Arabia": "sa",
    "Iran": "ir",
    "France": "fr",
    "Iraq": "iq",
    "Argentina": "ar",
    "Austria": "at",
    "Portugal": "pt",
    "England": "gb-eng",
    "Ghana": "gh",
    "Uzbekistan": "uz",
    "Czech Republic": "cz",
    "Switzerland": "ch",
    "Scotland": "gb-sct",
    "Turkey": "tr",
    "Ecuador": "ec",
    "Tunisia": "tn",
    "Uruguay": "uy",
    "New Zealand": "nz",
    "Norway": "no",
    "Jordan": "jo",
    "Panama": "pa",
    "Colombia": "co",
    "Bosnia and Herzegovina": "ba",
    "Morocco": "ma",
    "South Africa": "za",
    "Curaçao": "cw",
    "Japan": "jp",
    "Paraguay": "py",
    "Senegal": "sn",
    "Cape Verde": "cv",
    "Egypt": "eg",
    "Croatia": "hr",
    "DR Congo": "cd",
    "Algeria": "dz",
}

def flag_url(team):
    code = COUNTRY_CODE.get(team, "")
    return f"https://flagcdn.com/40x30/{code}.png" if code else ""

# Fetch data
url = "https://raw.githubusercontent.com/upbound-web/worldcup-live.json/master/2026/worldcup.json"
data = requests.get(url).json()

# Count goals
goal_counts = defaultdict(lambda: {"goals": 0, "team": ""})

for match in data['matches']:
    for col, team_key in [('goals1', 'team1'), ('goals2', 'team2')]:
        team = match.get(team_key, "")
        team = TEAM_NAME_FIX.get(team, team)
        for goal in match.get(col, []):
            if not goal.get('owngoal', False):
                name = goal['name']
                goal_counts[name]["goals"] += 1
                goal_counts[name]["team"] = team

top_scorers = sorted(goal_counts.items(), key=lambda x: x[1]["goals"], reverse=True)
for player, info in top_scorers:
    print(f"{info['team']} | {player}: {info['goals']}")

# Write to Google Sheets
sheet = client.open(SHEET_NAME).worksheet(TAB_NAME)
sheet.clear()
sheet.update(
    [['Player', 'Team', 'Flag', 'Goals']] +
    [[player, info['team'], flag_url(info['team']), info['goals']] for player, info in top_scorers]
)

print("Goalscorers updated successfully")
