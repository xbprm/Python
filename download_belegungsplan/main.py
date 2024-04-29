import requests
import os
import datetime
import logging

script_folder = os.path.dirname(os.path.abspath(__file__))
timestamp = datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
log_filename = f"script_log_{timestamp}.log"

# Configure logging to write to a new log file each run
logging.basicConfig(filename=os.path.join(script_folder, log_filename), level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# After configuring logging to file, add a console handler
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.INFO)  # Set the logging level for console output
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
console_handler.setFormatter(formatter)
logging.getLogger().addHandler(console_handler)

def prepend_new_log_to_main(new_log_path, main_log_path="script_log.log"):
    """
    Prepend the new log file's contents to the existing main log file.

    This function reads the contents of a newly created log file and prepends it
    to a main log file. If the main log file does not exist, it is created. This
    is useful for maintaining a chronological order of logs in a single file
    where the most recent logs appear at the beginning of the file.

    Parameters:
    - new_log_path (str): The file path of the new log file whose contents need to be prepended.
    - main_log_path (str, optional): The file path of the main log file to which the new log contents
      will be prepended. Defaults to "script_log.log".

    Returns:
    - None: This function does not return any value.

    Raises:
    - Exception: If an error occurs during the file operations, an exception is logged.
    """
    try:
        # Check if the main log file exists, create it if not
        if not os.path.exists(main_log_path):
            open(main_log_path, 'w').close()

        with open(new_log_path, 'r') as new_log_file:
            new_log_contents = new_log_file.read()
        with open(main_log_path, 'r+') as main_log_file:
            main_log_contents = main_log_file.read()
            main_log_file.seek(0, 0)
            main_log_file.write(new_log_contents + main_log_contents)
    except Exception as e:
        logging.error(f"Failed to prepend new log to main log: {e}")


def download_pdf(pdf_url, pdf_path):
    """
    Download a PDF file from a specified URL and save it to a given local path.

    This function attempts to download a PDF file from the provided URL. If the download is successful,
    the content is saved to the specified local file path. If any error occurs during the download or saving process,
    an error is logged, and the exception is raised to the caller.

    Parameters:
    - pdf_url (str): The URL from which the PDF file should be downloaded.
    - pdf_path (str): The local file path where the downloaded PDF should be saved.

    Raises:
    - requests.exceptions.RequestException: If an error occurs during the download process.

    Returns:
    - None
    """
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
    """
    Compare two files byte by byte to determine if they are identical.

    This function opens two files in binary read mode and compares their contents.
    If the contents of both files are exactly the same, it returns True, indicating
    the files are identical. Otherwise, it returns False. If an error occurs while
    attempting to open or read the files, the function logs the error and raises
    an IOError.

    Parameters:
    - file1 (str): The file path of the first file to compare.
    - file2 (str): The file path of the second file to compare.

    Returns:
    - bool: True if the files are identical, False otherwise.

    Raises:
    - IOError: If an error occurs during file opening or reading.
    """
    try:
        with open(file1, 'rb') as f1, open(file2, 'rb') as f2:
            return f1.read() == f2.read()
    except IOError as e:
        logging.error(f"File comparison error: {e}")
        raise

def backup_and_rename(original_path, new_path, backup_path):
    """
    Backup an original file by renaming it, then rename a new file to take the place of the original file.

    This function first renames the original file to a backup path, effectively creating a backup of the original.
    Then, it renames the new file to the original file's path, allowing the new file to replace the original file
    in its location. This process is useful for updating files while keeping a backup of the old version.

    Parameters:
    - original_path (str): The file path of the original file to be backed up.
    - new_path (str): The file path of the new file that will replace the original file.
    - backup_path (str): The file path where the original file will be renamed to, serving as its backup.

    Raises:
    - OSError: If an error occurs during the file renaming process.

    Returns:
    - None
    """
    try:
        os.rename(original_path, backup_path)  # Rename original file to backup path
        os.rename(new_path, original_path)  # Rename new file to original file's path
        logging.info(f"Original file backed up and new file renamed to original filename.")
    except OSError as e:
        logging.error(f"Error backing up and renaming files: {e}")
        raise  # Propagate the exception to the caller

def main():
    """
    Main function to execute the script's primary workflow.

    This function performs the following steps:
    1. Determines the current year and week number to generate filenames based on them.
    2. Downloads a PDF file from a specified URL.
    3. Checks if a file with the expected name for the current week already exists.
       - If it does and the contents are the same as the downloaded file, logs that information.
       - If the files are different, backs up the existing file with a timestamp and renames the downloaded file to match the expected filename.
       - If the expected file does not exist, renames the downloaded file to become the new expected file.

    No parameters are required for this function, and it does not return any values. It utilizes global variables for paths and logging configuration.
    """
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
    # After main script execution, prepend the new log file to the main log file
    new_log_path = os.path.join(script_folder, log_filename)
    main_log_path = os.path.join(script_folder, "script_log.log")
    prepend_new_log_to_main(new_log_path, main_log_path)
