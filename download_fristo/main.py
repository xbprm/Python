import requests
from bs4 import BeautifulSoup
import os
import fitz
import datetime
import webbrowser
import shutil

# script folder
script_folder = os.path.dirname(os.path.abspath(__file__))

# Get the current year and calendar week
current_year, current_week, _ = datetime.date.today().isocalendar()

search_terms = ["Rosbacher"]

# URL of the website you want to download and parse
url = "https://www.fristo.de/markt/schwalbach-am-taunus-am-flachsacker-32/"

# Send a GET request to the specified URL
response = requests.get(url)

# Check if the request was successful
if response.status_code == 200:
    # Use BeautifulSoup to parse the HTML content
    soup = BeautifulSoup(response.text, 'html.parser')
    
    # Example: Find all 'a' tags to get hyperlinks
    links = soup.find_all('a')
    
    # Print all the found links
    for link in links:
        if "dumpFile" in link.get('href'):
            url_angebote = link.get('href')
            # Download the file
            response_file = requests.get(url_angebote)
            # Modify the filename to include the current year and calendar week with two digits
            pdf_filename = f'downloaded_file_{current_year}_week_{current_week:02}.pdf'
            pdf_path = os.path.join(script_folder, pdf_filename)
            with open(pdf_path, 'wb') as file:
                file.write(response_file.content)

            # Open the PDF
            doc = fitz.open(pdf_path)
            # Flag to indicate if any term was found
            term_found = False
            found_term = ""

            # Check if any of the search terms was found and create an HTML file
            for page in doc:
                page_text = page.get_text()
                for term in search_terms:
                    if term in page_text:
                        term_found = True
                        found_term = term  # Store the found term
                        break  # Stop searching once any term is found
                if term_found:
                    break

            if term_found:
                title = f"{found_term} found"
            else:
                title = "Term NOT found"
                found_term = "No search term"  # Optional: Use this if you want to display a generic message or handle the case where no term is found.

            html_content = f"""
            <!DOCTYPE html>
            <html>
            <head>
                <title>{title}</title>
            </head>
            <body>
                <embed src="{pdf_filename}" type="application/pdf" width="100%" height="1024"/>
            </body>
            </html>
            """
            html_filename = f'pdf_embed_{current_year}_week_{current_week:02}.html'
            html_path = os.path.join(script_folder, html_filename)
            with open(html_path, 'w') as html_file:
                html_file.write(html_content)

            # Close the document
            doc.close()

            # Define the backup folder path
            backup_folder = os.path.join(script_folder, "backup")

            # Create the backup folder if it doesn't exist
            os.makedirs(backup_folder, exist_ok=True)

            # Copy the PDF and HTML files to the backup folder
            shutil.copy(pdf_path, backup_folder)
            shutil.copy(html_path, backup_folder)
            
            break

    # Open the HTML file in the default web browser
    webbrowser.open_new_tab(html_path)
             
else:
    print(f"Failed to retrieve the webpage: {response.status_code}")