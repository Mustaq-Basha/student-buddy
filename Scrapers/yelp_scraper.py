import requests
from bs4 import BeautifulSoup
import urllib.parse

def get_yelp_rating(name: str, city: str) -> float | None:
    query = f"{name} {city} site:yelp.com"
    search_url = f"https://www.google.com/search?q={urllib.parse.quote_plus(query)}"

    headers = {
        "User-Agent": "Mozilla/5.0",
    }

    try:
        res = requests.get(search_url, headers=headers, timeout=10)
        soup = BeautifulSoup(res.text, "html.parser")
        links = [a["href"] for a in soup.find_all("a", href=True) if "yelp.com/biz" in a["href"]]

        if links:
            yelp_url = links[0].split("&")[0].replace("/url?q=", "")
            res = requests.get(yelp_url, headers=headers, timeout=10)
            soup = BeautifulSoup(res.text, "html.parser")

            rating_tag = soup.select_one("div[aria-label*='star rating']")
            if rating_tag:
                rating_text = rating_tag["aria-label"]
                return float(rating_text.split()[0])
    except Exception as e:
        print(f"[Yelp] Error for {name}: {e}")

    return None
