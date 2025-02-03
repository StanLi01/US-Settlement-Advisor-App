import streamlit as st
import requests
import folium
from streamlit_folium import st_folium

def get_climate_data(lat, lon):
    """Fetch historical climate data from NASA POWER API"""
    url = f"https://power.larc.nasa.gov/api/temporal/climatology/point?parameters=T2M&community=SB&longitude={lon}&latitude={lat}&format=JSON"
    try:
        response = requests.get(url)
        response.raise_for_status()  # Raise an exception for bad responses
        data = response.json()
        return data['parameters']['T2M']  # Monthly avg temperature
    except (requests.RequestException, KeyError) as e:
        st.error(f"Error fetching climate data: {e}")
        return None

def main():
    st.title("Smart Settlement Advisor")
    st.write("Select a location to view historical climate and development trends.")
    
    # Map Selection
    st.subheader("Select a Location on the Map")
    m = folium.Map(location=[20, 0], zoom_start=2)
    
    # Input for coordinates
    col1, col2 = st.columns(2)
    with col1:
        lat = st.number_input("Latitude", min_value=-90.0, max_value=90.0, value=20.0, step=0.1)
    with col2:
        lon = st.number_input("Longitude", min_value=-180.0, max_value=180.0, value=0.0, step=0.1)
    
    # Add marker to the map
    folium.Marker([lat, lon], popup=f"Latitude: {lat}, Longitude: {lon}").add_to(m)
    
    # Use st_folium instead of folium_static
    output = st_folium(m, width=725)
    
    if st.button("Get Climate Data"):
        climate_data = get_climate_data(lat, lon)
        if climate_data:
            st.subheader("Historical Climate Data")
            st.write(f"Average monthly temperature (°C): {climate_data}")
        else:
            st.warning("Could not retrieve climate data for the selected location.")

if __name__ == "__main__":
    main()