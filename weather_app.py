import streamlit as st   
from geopy.geocoders import Nominatim   #load specific tool into geopy to convert city names to coordinates
#Nominatim is the actual geocoding engine — it uses OpenStreetMap data under the hood.

st.title("🌤️ Weather Forecast App")

city = st.text_input("Enter a city name", placeholder="e.g. Mumbai, London")  #Create a text box on the webpage.



if city:  #Only run the code below if the user has actually typed something. If the box is empty, do nothing.
    try:
        geolocator = Nominatim(user_agent="weather_app", timeout=10) #gives Nominatim 10 seconds instead of 1
        location = geolocator.geocode(city) #Send the city name to Nominatim
        if location:  #if Nominatim found the city, show the results. If it couldn't find it, go to the else block.
            st.success(f"Found: {location.address}")
            st.write(f"Latitude: {location.latitude}")
            st.write(f"Longitude: {location.longitude}")
        else:
            st.error("City not found. Try a different spelling.")

    except Exception as e: #catches the error and shows it nicely instead of crashing
        st.error(f"Connection error : {e}")
        