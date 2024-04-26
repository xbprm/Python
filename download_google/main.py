# Step 1: Set up Google Sheets API Access
# 1. # Go to the Google Developers Console (https://console.developers.google.com/).
# 2. Create a new project.
# 3. Enable the Google Sheets API for your project.
# 4. Create credentials (service account key) for your project.
# 5. Download the JSON file containing your credentials.
# 6. Share your Google sheet with the email address provided in your service account key (found in the JSON file).

# Step 2: Install Required Libraries
# You need to install gspread and pandas if you haven't already. You can do this using pip:
# pip install gspread pandas oauth2client

import gspread
from oauth2client.service_account import ServiceAccountCredentials
import pandas as pd

# Define the scope
scope = ['https://spreadsheets.google.com/feeds','https://www.googleapis.com/auth/drive']

# Add credentials to the account
creds = ServiceAccountCredentials.from_json_keyfile_name('path/to/your/credentials-file.json', scope)

# Authorize the clientsheet 
client = gspread.authorize(creds)

# Open the Google Sheet
sheet = client.open('Your Google Sheet Name')

# Get a list of all worksheets in the sheet
worksheets = sheet.worksheets()

# Initialize a dictionary to hold your DataFrames, keyed by sheet title
dfs = {}

# Iterate over each worksheet
for worksheet in worksheets:
    # Get all values in the current sheet
    data = worksheet.get_all_values()

    # Convert to a DataFrame
    df = pd.DataFrame(data[1:], columns=data[0])

    # Store the DataFrame in the dictionary, using the sheet title as the key
    dfs[worksheet.title] = df