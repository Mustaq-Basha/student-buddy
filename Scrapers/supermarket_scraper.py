import requests, pandas as pd

OVERPASS = "https://overpass-api.de/api/interpreter"
QUERY = """
[out:json];
area["name"="{city}"]->.searchArea;
node["shop"="supermarket"](area.searchArea);
out body;
"""

def get_supermarkets(city: str) -> pd.DataFrame:
    try:
        resp = requests.get(OVERPASS, params={"data": QUERY.format(city=city)})
        elements = resp.json().get("elements", [])
    except Exception as e:
        print("Scraper error:", e)
        return pd.DataFrame()

    rows = []
    for n in elements:
        lat, lon = n.get("lat"), n.get("lon")
        if lat is None or lon is None:
            continue
        rows.append({
            "Name": n.get("tags", {}).get("name", "Supermarket"),
            "Latitude": lat,
            "Longitude": lon,
            # Dummy fields so filters work (replace with real scraping later)
            "IndianSpices": False,
            "HasOffers": False,
            "Rating": 4.0,
        })
    return pd.DataFrame(rows)
