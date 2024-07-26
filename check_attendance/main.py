import os
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Set the path to the ChromeDriver executable
chrome_driver_path = r"C:\Util\chromedriver-win64"

# Define ChromeOptions
options = webdriver.ChromeOptions()

# Add the option for the executable path to ChromeDriver
options.add_argument(f"--executable-path={chrome_driver_path}")

# Create a ChromeDriver instance
driver = webdriver.Chrome(options)

# Define the URL of the website
url = "https://spieler.tennis.de/web/guest/turniersuche?tournamentId=638655"

# Navigate to the website
driver.get(url)

# Wait for the page to load completely (optional)
driver.implicitly_wait(10)  # Wait for 10 seconds

# Wait for the cookie consent button to appear and click it
cookie_button = WebDriverWait(driver, 10).until(
    EC.element_to_be_clickable((By.XPATH, "//button[@class='cookie-consent__button']"))
)
cookie_button.click()

# Wait for the page to load after accepting cookies
WebDriverWait(driver, 10).until(EC.staleness_of(cookie_button))

# Get the absolute path of the script file
script_path = os.path.abspath(__file__)

# Get the directory path of the script file
script_directory = os.path.dirname(script_path)

# Define the path to save the downloaded page
downloaded_page_path = os.path.join(script_directory, "downloaded_website.html")

# Save the page source to a file
with open(downloaded_page_path, "w", encoding="utf-8") as file:
    file.write(driver.page_source)

# Close the ChromeDriver instance
driver.quit()

# Define string to search for
string_to_search = r"Herren 40 Einzel"