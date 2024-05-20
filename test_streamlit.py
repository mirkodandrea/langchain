import streamlit as st
import folium
from streamlit_folium import folium_static
import time

# Sample get_latest_news function that simulates fetching data with a delay

from get_latest_news import get_latest_news, get_latest_news_urls

# Title of the app
st.title("Wildfire Incidents Map Visualization")

# Input box for country
country = st.text_input("Enter a country to search for wildfire incidents:")

# Button to update the news
if st.button('Update'):
    with st.spinner('Fetching the latest urls...'):
        urls = get_latest_news_urls(country)

    with st.spinner(f'Processing {len(urls)} articles...'):
        results = get_latest_news(urls)

    # Calculate the bounding box to fit all markers

    # Initialize the map
    map_ = folium.Map()

    incidents = []
    # Add markers to the map

    for incident in results:
        lat, lon = incident["approximate_location"]
        popup_content = f"""
        <strong>Date:</strong> {incident['date']}<br>
        <strong>Country:</strong> {incident['country']}<br>
        <strong>Description:</strong> {incident['description']}<br>
        <strong>Affected Population:</strong> {incident['affected_population'] if incident['affected_population'] else 'N/A'}<br>
        <strong>Relevant:</strong> {'Yes' if incident['relevant'] else 'No'}<br>
        <a href="{incident['url']}" target="_blank">More Info</a>
        """
        popup = folium.Popup(popup_content, max_width=300)
        folium.Marker(
            [lat, lon],
            popup=popup,
            tooltip=incident["description"]
        ).add_to(map_)

    bounds = [[incident["approximate_location"][0],
               incident["approximate_location"][1]] for incident in results]

    folium_static(map_)
    map_.fit_bounds(bounds)
