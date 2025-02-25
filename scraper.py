import requests
from bs4 import BeautifulSoup

def scrape_text(url):
    response = requests.get(url, timeout=10)
    if response.status_code != 200:
        return f"Failed to fetch {url}"
    soup = BeautifulSoup(response.text, "html.parser")
    return soup.get_text(separator=" ", strip=True)
