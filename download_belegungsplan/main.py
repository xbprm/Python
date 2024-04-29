import requests
import os
import datetime
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def download_pdf(pdf_url, pdf_path):
    """Download PDF from a given URL and save it to a specified path."""
    try:
        response = requests.get(pdf_url)
        response.raise_for_status()  # Raises an HTTPError for bad responses
        with open(pdf_path, 'wb') as file:
            file.write(response.content)
        logging.info(f"PDF downloaded successfully: {pdf_path}")
    except requests.exceptions.RequestException as e:
        logging.error(f"Failed to download PDF: {e}")
        raise

def compare_files(file1, file2):
    """Compare two files byte by byte."""
    try:
        with open(file1, 'rb') as f1, open(file2, 'rb') as f2:
            return f1.read() == f2.read()
    except IOError as e:
        logging.error(f"File comparison error: {e}")
        raise

def backup_and_rename(original_path, new_path, backup_path):
    """Backup the original file and rename the new file to the original file's name."""
    try:
        os.rename(original_path, backup_path)
        os.rename(new_path, original_path)
        logging.info(f"Original file backed up and new file renamed to original filename.")
    except OSError as e:
        logging.error(f"Error backing up and renaming files: {e}")
        raise

def main():
    script_folder = os.path.dirname(os.path.abspath(__file__))
    current_year, current_week, _ = datetime.date.today().isocalendar()
    pdf_url = "http://www.platzbelegung.tennis65-eschborn.de/Platzbelegung-Woche.pdf"
    pdf_filename = f'downloaded_file_{current_year}_week_{current_week:02}.pdf'
    pdf_path = os.path.join(script_folder, pdf_filename)

    download_pdf(pdf_url, pdf_path)

    belegungsplan_filename = f'belegungsplan_{current_year}_week_{current_week:02}.pdf'
    belegungsplan_path = os.path.join(script_folder, belegungsplan_filename)

    if os.path.exists(belegungsplan_path):
        if compare_files(belegungsplan_path, pdf_path):
            logging.info("The downloaded file is the same as the original file.")
        else:
            logging.info("The downloaded file is different from the original file.")
            timestamp = datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
            backup_filename = f'belegungsplan_{current_year}_week_{current_week:02}_{timestamp}.pdf'
            backup_path = os.path.join(script_folder, backup_filename)
            backup_and_rename(belegungsplan_path, pdf_path, backup_path)
    else:
        logging.info("The original file does not exist. Renaming the downloaded file to the original filename.")
        os.rename(pdf_path, belegungsplan_path)

if __name__ == "__main__":
    main()