import streamlit as st
import folium
from streamlit_folium import st_folium
import requests

def get_weather_data(state):
    """Fetch current weather data using OpenWeatherMap API"""
    api_key = st.secrets.get("OPENWEATHER_API_KEY")
    state_centers = {
        'California': {'lat': 36.7783, 'lon': -119.4179},
        'Texas': {'lat': 31.9686, 'lon': -99.9018}
    }
    
    try:
        location = state_centers.get(state, {'lat': 0, 'lon': 0})
        url = f"https://api.openweathermap.org/data/2.5/weather?lat={location['lat']}&lon={location['lon']}&appid={api_key}&units=imperial"
        response = requests.get(url)
        data = response.json()
        return {
            'temperature': data['main']['temp'],
            'description': data['weather'][0]['description']
        }
    except Exception as e:
        st.error(f"Weather data error: {e}")
        return None

def get_population_data(state):
    """Fetch population data from US Census Bureau API"""
    api_key = st.secrets.get("CENSUS_API_KEY")
    try:
        url = f"https://api.census.gov/data/2021/pep/population?get=NAME,POP&for=state:*&key={api_key}"
        response = requests.get(url)
        data = response.json()
        
        # Find state's population
        for entry in data[1:]:  # Skip header
            if state.upper() in entry[0]:
                return {
                    'current_population': int(entry[1]),
                    'population_change': 'Tracking...'  # Requires more complex API call
                }
        return None
    except Exception as e:
        st.error(f"Population data error: {e}")
        return None

def get_crime_data(state):
    """Fetch crime data from FBI Crime Data API"""
    api_key = st.secrets.get("FBI_CRIME_API_KEY")
    try:
        # Note: Actual FBI API might require different endpoint
        url = f"https://api.fbi.gov/crime-data/{state.lower()}"
        response = requests.get(url)
        data = response.json()
        return {
            'violent_crime_rate': data.get('violent_crime_rate', 'N/A'),
            'property_crime_rate': data.get('property_crime_rate', 'N/A')
        }
    except Exception as e:
        st.error(f"Crime data error: {e}")
        return None

def create_us_map():
    """Create a Folium map focused on the United States"""
    m = folium.Map(location=[39.8283, -98.5795], zoom_start=4)
    return m

def main():
    st.title("US Settlement Advisor")
    
    # State selection
    states = ['California', 'Texas']
    selected_state = st.selectbox("Select a State", states)
    
    # Fetch data from APIs
    weather_data = get_weather_data(selected_state)
    population_data = get_population_data(selected_state)
    crime_data = get_crime_data(selected_state)
    
    # Display data
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.subheader("Weather")
        if weather_data:
            st.metric("Temperature", f"{weather_data['temperature']}°F")
            st.write(f"Conditions: {weather_data['description']}")
    
    with col2:
        st.subheader("Population")
        if population_data:
            st.metric("Current Population", f"{population_data['current_population']:,}")
    
    with col3:
        st.subheader("Crime")
        if crime_data:
            st.metric("Violent Crime Rate", str(crime_data['violent_crime_rate']))
    
    # Interactive map
    m = create_us_map()
    st_folium(m, width=725)

if __name__ == "__main__":
    main()
