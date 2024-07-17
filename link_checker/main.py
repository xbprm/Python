import requests
from bs4 import BeautifulSoup
import re

# Set to store unique links
visited_links = set()

def parse_website(url, output_file, url_prefix=""):
    """
    This function parses a given website and extracts all valid links and file links.
    It writes the extracted links to an output file and recursively parses linked sites.

    Parameters:
    url (str): The URL of the website to parse.
    output_file (str): The name of the output file where the extracted links will be written.
    url_prefix (str, optional): The URL prefix to filter valid links. Defaults to "https://www.fristo.de".

    Returns:
    None
    """
    try:
        response = requests.get(url)
        response.raise_for_status()  # Raise an exception for 4xx or 5xx status codes
        soup = BeautifulSoup(response.content, 'html.parser')

        # Find all anchor tags
        anchor_tags = soup.find_all('a')

        for tag in anchor_tags:
            href = tag.get('href')

            # Check if the href attribute starts with "https"
            if href and href.startswith(url_prefix):
                # Check if the link is already visited
                if href not in visited_links:
                    visited_links.add(href)
                    print(f"Found valid link: {href}")
                    with open(output_file, 'a') as f:
                        f.write(f"{href}\n")
                    parse_website(href, output_file, url_prefix)  # Recursively parse the linked site

            elif href and re.search(r'\.(pdf|jpg|png|docx|xlsx|csv)$', href, re.IGNORECASE):
                print(f"Found file link: {href}")
                with open(output_file, 'a') as f:
                    f.write(f"{href}\n")

    except requests.exceptions.RequestException as e:
        print(f"Error accessing {url}: {e}")

# Usage example
url_start = "https://www.fristo.de/markt/schwalbach-am-taunus-am-flachsacker-32/"
parse_website(url_start, "links.txt", "https://www.fristo.de")