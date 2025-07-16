import requests, re

SPICE_KEYWORDS = ["garam", "masala", "turmeric", "curry powder", "indian spice"]
OFFERS_KEYWORDS = ["angebot", "angebote", "discount", "sale"]

def check_site_for_info(domain: str) -> dict:
    """
    Fetch homepage (or `/de/` page) and look for spice/offers keywords.
    Returns {'IndianSpices': bool, 'HasOffers': bool}
    """
    try:
        html = requests.get(f"https://{domain}", timeout=6).text.lower()
    except Exception:
        return {"IndianSpices": False, "HasOffers": False}

    indian = any(kw in html for kw in SPICE_KEYWORDS)
    offers = any(kw in html for kw in OFFERS_KEYWORDS)
    return {"IndianSpices": indian, "HasOffers": offers}

# Map brand name → domain
BRAND_DOMAIN = {
    "rewe": "rewe.de",
    "edeka": "edeka.de",
    "lidl": "lidl.de",
    "aldi": "aldi-nord.de",
}

def enrich_spices_offers(row):
    name_lower = row["Name"].lower()
    domain = None
    for brand, dom in BRAND_DOMAIN.items():
        if brand in name_lower:
            domain = dom
            break
    if not domain:
        return {"IndianSpices": False, "HasOffers": False}
    return check_site_for_info(domain)
