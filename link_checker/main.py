import requests
from bs4 import BeautifulSoup
import re
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time

# Set to store unique links
visited_links = set()

def parse_website(url, output_file, url_prefix="", depth=0, max_depth=4):
    """
    This function parses a given website and extracts all valid links and file links.
    It writes the extracted links to an output file and recursively parses linked sites.

    Parameters:
    url (str): The URL of the website to parse.
    output_file (str): The name of the output file where the extracted links will be written.
    url_prefix (str, optional): The URL prefix to filter valid links. Defaults to "https://www.fristo.de".
    depth (int, optional): The current depth of recursion. Defaults to 0.
    max_depth (int, optional): The maximum depth of recursion. Defaults to 4.

    Returns:
    None
    """
    if depth > max_depth:
        return

    try:
        print(f"Parsing {url}")

        # Set up Selenium with ChromeDriver
        chrome_options = Options()
        chrome_options.add_argument("--headless")  # Run Chrome in headless mode
        driver = webdriver.Chrome(options=chrome_options)

        driver.get(url)
        time.sleep(5)  # Wait for the page to load completely

        print("Parsing complete")
        soup = BeautifulSoup(driver.page_source, 'html.parser')
        print(soup.prettify()[:1000] + "...\n")

        # Find all anchor tags
        anchor_tags = soup.find_all('a')
        print("Links found:", len(anchor_tags))

        for tag in anchor_tags:
            href = tag.get('href')
            print(f"Found href: {href}")

            # Check if the href attribute starts with "https"
            if href and href.startswith(url_prefix):
                # Check if the link is already visited
                if href not in visited_links:
                    visited_links.add(href)
                    print(f"Found valid link: {href}")
                    with open(output_file, 'a') as f:
                        f.write(f"{href}\n")
                    parse_website(href, output_file, url_prefix, depth + 1, max_depth)  # Recursively parse the linked site

            elif href and re.search(r'\.(pdf|jpg|png|docx|xlsx|csv)$', href, re.IGNORECASE):
                print(f"Found file link: {href}")
                with open(output_file, 'a') as f:
                    f.write(f"{href}\n")

        driver.quit()

    except Exception as e:
        print(f"Error accessing {url}: {e}")

# Usage example
url_start = "https://processes.cw01.contiwan.com/stages/#/workspace/7854/_vv/process/artifact/_ZEEPMDChmoG72b4zdxAJZQ"
parse_website(url_start, "links.txt", "https://processes.cw01.contiwan.com", max_depth=4)