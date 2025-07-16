import streamlit as st
from streamlit_folium import st_folium
from geopy.distance import geodesic
import pandas as pd
import time

from Scrapers.supermarket_scraper import get_supermarkets
from Scrapers.multi_source_scraper import enrich_supermarket_info
from utils.location_utils import get_location_coordinates
from utils.map_utils import render_map

st.set_page_config(page_title="Student City Buddy", layout="wide")
st.title("🇩🇪 Student City Buddy")
st.write("Find supermarkets near your university with live distance & filters.")

# Session-state defaults
for key in ["df_supermarkets", "uni_lat", "uni_lon", "university_name"]:
    st.session_state.setdefault(key, None)

left, _ = st.columns([1, 2])

with left:
    st.header("Inputs")
    city = st.text_input("City", "Koblenz")

    # Dropdown if we know city; otherwise allow manual entry
    uni_options = {
        "Koblenz": [
            "University of Koblenz",
            "Hochschule Koblenz",
            "WHU – Otto Beisheim School of Management"
        ],
        "Berlin": [
            "Humboldt University of Berlin",
            "TU Berlin",
            "Free University of Berlin"
        ],
        "Munich": [
            "Technical University of Munich",
            "Ludwig‑Maximilians‑Universität München"
        ]
    }
    university_name = (
        st.selectbox("University", uni_options.get(city, ["Enter manually"]))
        if city in uni_options else
        st.text_input("University name")
    )

    st.markdown("### Filters")
    indian_only = st.checkbox("Indian spices available")
    offers_only = st.checkbox("Has offers / discounts")
    min_rating = st.slider("Min rating", 0.0, 5.0, 3.5, 0.1)

    if st.button("Find Supermarkets"):
        # Get university coordinates
        uni_lat, uni_lon = get_location_coordinates(university_name)
        st.session_state.uni_lat = uni_lat
        st.session_state.uni_lon = uni_lon
        st.session_state.university_name = university_name

        # Get base supermarkets (lat/lon)
        base_df = get_supermarkets(city)
        if base_df is None or base_df.empty:
            st.warning("No supermarkets found.")
        else:
            enriched_rows = []
            with st.spinner("Scraping additional info..."):
                for _, row in base_df.iterrows():
                    enrichments = enrich_supermarket_info(row["Name"], city)
                    enriched_rows.append({
                        **row,
                        "Rating": enrichments.get("rating", 0),
                        "IndianSpices": enrichments.get("indian_spices", False),
                        "HasOffers": enrichments.get("offers", False),
                    })
                    time.sleep(1)  # prevent overloading Yelp/TripAdvisor

            df = pd.DataFrame(enriched_rows)

            # Filters
            if indian_only:
                df = df[df["IndianSpices"] == True]
            if offers_only:
                df = df[df["HasOffers"] == True]
            df = df[df["Rating"] >= min_rating]

            # Distance from university
            if uni_lat and uni_lon:
                df["distance_km"] = df.apply(
                    lambda r: geodesic((uni_lat, uni_lon), (r["Latitude"], r["Longitude"])).km,
                    axis=1
                )
            else:
                df["distance_km"] = None

            st.session_state.df_supermarkets = df

# ---- Map (persists between reruns) ----
df_map = st.session_state.df_supermarkets
m = render_map(
    st.session_state.university_name,
    st.session_state.uni_lat,
    st.session_state.uni_lon,
    df_map
)
st_folium(m, width=1000, height=700)

# Optional: debug preview
if df_map is not None:
    st.write("### 🐞 Debug preview")
    st.dataframe(df_map)
