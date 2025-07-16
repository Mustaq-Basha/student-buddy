import os, requests, time

GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")  # put your key in env var

ENDPOINT_FIND = "https://maps.googleapis.com/maps/api/place/findplacefromtext/json"
ENDPOINT_DETAILS = "https://maps.googleapis.com/maps/api/place/details/json"

def get_place_rating(name: str, lat: float, lon: float, city: str) -> dict:
    """
    Returns {'rating': float|None, 'user_ratings_total': int|None} via Places API.
    """
    if not GOOGLE_API_KEY:
        return {"rating": None, "user_ratings_total": None}

    query = f"{name} {city}"
    params = {
        "input": query,
        "inputtype": "textquery",
        "fields": "place_id",
        "locationbias": f"point:{lat},{lon}",
        "key": GOOGLE_API_KEY,
    }
    try:
        r = requests.get(ENDPOINT_FIND, params=params).json()
        candidates = r.get("candidates", [])
        if not candidates:
            return {"rating": None, "user_ratings_total": None}

        place_id = candidates[0]["place_id"]
        details = requests.get(
            ENDPOINT_DETAILS,
            params={
                "place_id": place_id,
                "fields": "rating,user_ratings_total",
                "key": GOOGLE_API_KEY,
            },
        ).json()
        result = details.get("result", {})
        return {
            "rating": result.get("rating"),
            "user_ratings_total": result.get("user_ratings_total"),
        }
    except Exception as e:
        print("Google API error:", e)
        return {"rating": None, "user_ratings_total": None}
