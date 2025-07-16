import streamlit as st
from geopy.geocoders import Nominatim
from geopy.distance import geodesic
import pandas as pd

# 🧠 Cache the coordinates for performance
@st.cache_data(show_spinner=False, ttl=3600)
def get_location_coordinates(place_name: str):
    """
    Get latitude and longitude for a given place using Nominatim.
    Uses known address overrides for better accuracy.
    """
    known_universities = {
        "university of koblenz": "Universitätsstraße 1, 56070 Koblenz",
        "hochschule koblenz": "Konrad-Zuse-Straße 1, 56075 Koblenz",
        # Add more overrides as needed
    }

    place_name_lower = place_name.strip().lower()
    if place_name_lower in known_universities:
        place_name = known_universities[place_name_lower]

    geolocator = Nominatim(user_agent="student_city_buddy")
    try:
        location = geolocator.geocode(place_name, timeout=10)
        if location:
            return location.latitude, location.longitude
    except Exception as e:
        print(f"Geolocation error for '{place_name}': {e}")
    return None, None

# 🔁 Sort results by distance from university
def sort_by_distance(df: pd.DataFrame, ref_point: tuple):
    """
    Add a 'distance_km' column to the DataFrame and sort it.
    """
    df["distance_km"] = df.apply(
        lambda row: geodesic(ref_point, (row["Latitude"], row["Longitude"])).km,
        axis=1
    )
    return df.sort_values("distance_km")

# 🎯 Filter within a radius
def filter_by_proximity(df: pd.DataFrame, ref_point: tuple, radius_km: float):
    """
    Return only rows within a radius_km from ref_point.
    """
    if "distance_km" not in df.columns:
        df = sort_by_distance(df, ref_point)
    return df[df["distance_km"] <= radius_km].reset_index(drop=True)

# 📏 Minimum distance for display info
def get_shortest_distance_to_supermarket(df: pd.DataFrame, university_coords: tuple) -> float:
    """
    Returns the distance (in km) to the nearest supermarket.
    """
    if df.empty or not university_coords:
        return None
    distances = df.apply(
        lambda row: geodesic(university_coords, (row['Latitude'], row['Longitude'])).km,
        axis=1
    )
    return distances.min()
