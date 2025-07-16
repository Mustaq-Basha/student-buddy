import folium, pandas as pd
from geopy.distance import geodesic

def render_map(university, uni_lat, uni_lon, df):
    center = [uni_lat, uni_lon] if uni_lat and uni_lon else [50.3569, 7.5889]
    m = folium.Map(location=center, zoom_start=13)

    if uni_lat and uni_lon:
        folium.Marker(
            [uni_lat, uni_lon],
            popup=f"{university} 🎓",
            icon=folium.Icon(color="green", icon="university", prefix="fa")
        ).add_to(m)

    if df is not None and not df.empty:
        for _, row in df.iterrows():
            popup = row["Name"]
            if "distance_km" in row and pd.notna(row["distance_km"]):
                popup += f" ({row['distance_km']:.2f} km)"
            folium.Marker(
                [row["Latitude"], row["Longitude"]],
                popup=popup,
                icon=folium.Icon(color="blue", icon="shopping-cart", prefix="fa")
            ).add_to(m)
    return m
