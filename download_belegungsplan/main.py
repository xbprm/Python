import requests
import os
import datetime

# Determine the script's directory for file operations
script_folder = os.path.dirname(os.path.abspath(__file__))

# Get the current year and calendar week for naming files
current_year, current_week, _ = datetime.date.today().isocalendar()

# Download the PDF
pdf_url = "http://www.platzbelegung.tennis65-eschborn.de/Platzbelegung-Woche.pdf"
response_file = requests.get(pdf_url)

# Create a filename that includes the current year and week
pdf_filename = f'downloaded_file_{current_year}_week_{current_week:02}.pdf'
pdf_path = os.path.join(script_folder, pdf_filename)
with open(pdf_path, 'wb') as file:
    file.write(response_file.content)

# compare the downloaded file with the original file
belegungsplan_filename = f'belegungsplan_{current_year}_week_{current_week:02}.pdf'
belegungsplan_path = os.path.join(script_folder, belegungsplan_filename)

if os.path.exists(belegungsplan_path):
    with open(belegungsplan_path, 'rb') as original_file:
        with open(pdf_path, 'rb') as downloaded_file:
            if original_file.read() == downloaded_file.read():
                print('The downloaded file is the same as the original file.')
            else:
                print('The downloaded file is different from the original file.')
                # get the current timstamp
                timestamp = datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
                # create a backup file
                backup_filename = f'belegungsplan_{current_year}_week_{current_week:02}_{timestamp}.pdf'
                backup_path = os.path.join(script_folder, backup_filename)
                original_file.close()
                os.rename(belegungsplan_path, backup_path)
                # rename the downloaded file to the original filename
                downloaded_file.close()                
                os.rename(pdf_path, belegungsplan_path)
                print('The downloaded file has been renamed to the original filename.')
else:
    print('The original file does not exist.')

    # rename the downloaded file to the original filename
    os.rename(pdf_path, belegungsplan_path)
    print('The downloaded file has been renamed to the original filename.')
