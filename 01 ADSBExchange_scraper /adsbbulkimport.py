import os
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin

# URL of the page to scrape
base_url = 'https://samples.adsbexchange.com/readsb-hist/2024/05/01/'

# Directory to save downloaded files
download_dir = '/Users/jonathonmason/Downloads/ADSBExchange_files/'

# Ensure the download directory exists
os.makedirs(download_dir, exist_ok=True)

# Function to download a file
def download_file(url, directory):
    local_filename = os.path.join(directory, url.split('/')[-1])
    with requests.get(url, stream=True) as r:
        r.raise_for_status()
        with open(local_filename, 'wb') as f:
            for chunk in r.iter_content(chunk_size=8192):
                f.write(chunk)
    return local_filename

# Scrape the web page for links to .json.gz files
response = requests.get(base_url)
soup = BeautifulSoup(response.content, 'html.parser')

# Find all links on the page
links = soup.find_all('a')

# Filter links that end with .json.gz
file_links = [link.get('href') for link in links if link.get('href').endswith('.json.gz')]

# Download each file
for file_link in file_links:
    file_url = urljoin(base_url, file_link)
    print(f"Downloading {file_url}")
    download_file(file_url, download_dir)

print("All files downloaded.")
