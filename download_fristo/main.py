import requests
from bs4 import BeautifulSoup
import os
import fitz  # PyMuPDF
import datetime
import webbrowser
import shutil

# Determine the script's directory for file operations
script_folder = os.path.dirname(os.path.abspath(__file__))

# Get the current year and calendar week for naming files
current_year, current_week, _ = datetime.date.today().isocalendar()

# List of search terms to find within the PDF document
search_terms = ["Rosbacher"]

# URL of the website to download the PDF from
url = "https://www.fristo.de/markt/schwalbach-am-taunus-am-flachsacker-32/"

# Send a GET request to the website
response = requests.get(url)

# Check if the request was successful
if response.status_code == 200:
    # Parse the HTML content of the page
    soup = BeautifulSoup(response.text, 'html.parser')
    
    # Find all 'a' tags to locate hyperlinks
    links = soup.find_all('a')
    
    # Loop through all found links to find the download link
    for link in links:
        if "dumpFile" in link.get('href'):
            url_angebote = link.get('href')
            # Download the PDF file from the found URL
            response_file = requests.get(url_angebote)
            # Create a filename that includes the current year and week
            pdf_filename = f'downloaded_file_{current_year}_week_{current_week:02}.pdf'
            pdf_path = os.path.join(script_folder, pdf_filename)
            with open(pdf_path, 'wb') as file:
                file.write(response_file.content)

            # Open the downloaded PDF file for reading
            doc = fitz.open(pdf_path)
            # Initialize a flag to indicate if the search term was found
            term_found = False
            found_term = ""

            # Search each page of the PDF for the search terms
            for page in doc:
                page_text = page.get_text()
                for term in search_terms:
                    if term in page_text:
                        term_found = True
                        found_term = term  # Save the found term
                        break  # Exit the loop once a term is found
                if term_found:
                    break

            # Prepare the title for the HTML file based on search result
            if term_found:
                title = f"{found_term} found"
            else:
                title = "Term NOT found"
                found_term = "No search term"  # Placeholder for no search term found

            # Generate HTML content to embed the PDF
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
            # Create a filename for the HTML file
            html_filename = f'pdf_embed_{current_year}_week_{current_week:02}.html'
            html_path = os.path.join(script_folder, html_filename)
            with open(html_path, 'w') as html_file:
                html_file.write(html_content)

            # Close the PDF document to free resources
            doc.close()

            # Specify the backup folder and ensure its existence
            backup_folder = os.path.join(script_folder, "backup")
            os.makedirs(backup_folder, exist_ok=True)

            # Copy the PDF and HTML files to the backup directory
            shutil.copy(pdf_path, backup_folder)
            shutil.copy(html_path, backup_folder)
            
            break  # Exit the loop after processing the first matching link

    # Open the generated HTML file in the default web browser
    webbrowser.open_new_tab(html_path)
             
else:
    # Log an error message if the webpage could not be retrieved
    print(f"Failed to retrieve the webpage: {response.status_code}")