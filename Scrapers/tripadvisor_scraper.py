import requests
from bs4 import BeautifulSoup
import urllib.parse
import time

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0 Safari/537.36"
}

def get_tripadvisor_rating(name: str, city: str) -> float | None:
    """Scrapes TripAdvisor search results and returns the first star rating found."""
    try:
        # Construct Google Search URL targeting TripAdvisor
        query = f"{name} {city} site:tripadvisor.com"
        url = f"https://www.google.com/search?q={urllib.parse.quote(query)}"

        response = requests.get(url, headers=HEADERS, timeout=10)
        if response.status_code != 200:
            print(f"[TripAdvisor] Failed to fetch Google search for {name}")
            return None

        soup = BeautifulSoup(response.text, "html.parser")

        # Look for rating snippets (often shown as ★★★★☆ or 4.3)
        rating_tags = soup.find_all("span")
        for tag in rating_tags:
            text = tag.get_text(strip=True)
            if text and text.replace(".", "", 1).isdigit():
                val = float(text)
                if 1 <= val <= 5:
                    return val
        return None
    except Exception as e:
        print(f"[TripAdvisor] Error for {name}: {e}")
        return None
