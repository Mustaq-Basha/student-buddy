import folium
from geopy.distance import geodesic

def render_map(university_name, uni_lat, uni_lon, df):
    # Default center: Koblenz if university location isn't found
    map_center = [uni_lat, uni_lon] if uni_lat and uni_lon else [50.3569, 7.5889]
    m = folium.Map(location=map_center, zoom_start=13)

    # University Marker
    if uni_lat and uni_lon:
        folium.Marker(
            location=[uni_lat, uni_lon],
            popup=f"{university_name} 🎓",
            icon=folium.Icon(color="green", icon="university", prefix="fa")
        ).add_to(m)

    # Supermarket Markers with distance in popup
    if df is not None and not df.empty:
        for _, row in df.iterrows():
            popup_text = row["Name"]
            if uni_lat and uni_lon:
                supermarket_coords = (row["Latitude"], row["Longitude"])
                university_coords = (uni_lat, uni_lon)
                distance_km = geodesic(university_coords, supermarket_coords).km
                popup_text += f" ({distance_km:.2f} km)"

            folium.Marker(
                location=[row["Latitude"], row["Longitude"]],
                popup=popup_text,
                icon=folium.Icon(color="blue", icon="shopping-cart", prefix="fa")
            ).add_to(m)

    return m
