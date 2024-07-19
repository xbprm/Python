from selenium import webdriver

# Set the path to the ChromeDriver executable
chrome_driver_path = r"C:\Util\chromedriver-win64"

# define ChromeOptions
options = webdriver.ChromeOptions()

# add the option for the executable path to ChromeDriver
options.add_argument(f"--executable-path={chrome_driver_path}")

# Create a ChromeDriver instance
driver = webdriver.Chrome(options)

# Define the URL of the website
url = "https://spieler.tennis.de/web/guest/turniersuche?tournamentId=638655"

# Navigate to the website
driver.get(url)

# Wait for the page to load completely (optional)
driver.implicitly_wait(10)  # Wait for 10 seconds

# Save the page source to a file
with open("downloaded_website.html", "w", encoding="utf-8") as file:
    file.write(driver.page_source)

# Close the ChromeDriver instance
driver.quit()

# define string to search for
string_to_search = r"Herren 40 Einzel"

