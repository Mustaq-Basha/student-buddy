from Scrapers.yelp_scraper import get_yelp_rating
from Scrapers.tripadvisor_scraper import get_tripadvisor_rating

def enrich_supermarket_info(name: str, city: str) -> dict:
    """Returns rating, spice info, and offers status for a supermarket."""
    rating = get_yelp_rating(name, city)
    #if not rating:
        #rating = get_tripadvisor_rating(name, city)

    # NOTE: These are dummy for now
    has_indian_spices = "Indian" in name or "Spice" in name
    has_offers = "Discount" in name or "Sale" in name

    return {
        "rating": rating or 0.0,
        "indian_spices": has_indian_spices,
        "offers": has_offers,
    }
