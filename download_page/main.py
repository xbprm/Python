import requests
from bs4 import BeautifulSoup
import re

# Specify the URL of the webpage to download
url = 'https://www.mein-aramark-restaurant.de/menu/Continental%20Automotive%20Technologies%20GmbH%20Frankfurt/Continental%20Frankfurt%20-%20Betriebsrestaurant'

# Use the requests library to download the webpage
response = requests.get(url)

# Parse the downloaded HTML
soup = BeautifulSoup(response.text, 'html.parser')
print(soup.prettify())

# Use the BeautifulSoup library to search for the specified string
results = soup.find_all(string=re.compile('14'))

# Print the number of results found
print(f'Found {len(results)} results')