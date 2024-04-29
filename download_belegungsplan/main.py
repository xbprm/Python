import requests
import fitz  # PyMuPDF
import pandas as pd

# Download the PDF
pdf_url = "http://www.platzbelegung.tennis65-eschborn.de/Platzbelegung-Woche.pdf"
response = requests.get(pdf_url)
with open('downloaded_file.pdf', 'wb') as f:
    f.write(response.content)

# compare the downloaded file with the original file
