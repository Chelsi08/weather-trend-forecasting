import streamlit as st
import requests
from geopy.geocoders import Nominatim
from datetime import datetime, timedelta

st.title("🌤️ Weather Forecast App")
st.markdown("Real-time weather forecast for any city — up to 16 days ahead.")
st.markdown("---")

city = st.text_input("Enter a city name", placeholder="e.g. Mumbai, London, New York")

if city:
    try:
        geolocator = Nominatim(user_agent="weather_app", timeout=10)
        location = geolocator.geocode(city)

        if location:
            st.success(f"📍 Found: {location.address}")
            lat = location.latitude
            lon = location.longitude

            target_date = st.date_input(
                "🗓️ Select a date",
                value=datetime.today().date(),
                min_value=datetime.today().date(),
                max_value=(datetime.today() + timedelta(days=16)).date()
            )

            days_from_today = (target_date - datetime.today().date()).days

            # ── Open-Meteo API call ────────────────────────────────────────
            response = requests.get(
                "https://api.open-meteo.com/v1/forecast",
                params={
                    "latitude": lat,
                    "longitude": lon,
                    "daily": [
                        "temperature_2m_max",
                        "temperature_2m_min",
                        "precipitation_sum",
                        "windspeed_10m_max",
                        "relative_humidity_2m_mean"
                    ],
                    "current_weather": True,
                    "timezone": "auto",
                    "forecast_days": 16
                }
            )

            data = response.json()
            daily_api = data["daily"]
            dates = daily_api["time"]
            current = data.get("current_weather", {})

            # ── Current conditions ─────────────────────────────────────────
            if days_from_today == 0 and current:
                st.subheader("🌡️ Current Conditions")
                c1, c2 = st.columns(2)
                c1.metric("Temperature", f"{current.get('temperature', 'N/A')}°C")
                c2.metric("Wind Speed",  f"{current.get('windspeed', 'N/A')} km/h")
                st.markdown("---")

            # ── Forecast for selected date ─────────────────────────────────
            target_str = str(target_date)

            if target_str in dates:
                idx = dates.index(target_str)

                st.subheader(f"📅 Forecast for {city} on {target_date}")

                col1, col2, col3, col4, col5 = st.columns(5)
                col1.metric("🌡️ Max Temp",      f"{daily_api['temperature_2m_max'][idx]}°C")
                col2.metric("🌡️ Min Temp",      f"{daily_api['temperature_2m_min'][idx]}°C")
                col3.metric("🌧️ Precipitation", f"{daily_api['precipitation_sum'][idx]} mm")
                col4.metric("💨 Max Wind",       f"{daily_api['windspeed_10m_max'][idx]} km/h")
                col5.metric("💧 Humidity",       f"{daily_api['relative_humidity_2m_mean'][idx]}%")

                # ── 16-day chart ───────────────────────────────────────────
                st.markdown("---")
                st.subheader("📈 16-Day Temperature Forecast")

                import plotly.graph_objects as go
                import pandas as pd

                df_chart = pd.DataFrame({
                    'Date':         pd.to_datetime(dates),
                    'Max Temp (°C)': daily_api['temperature_2m_max'],
                    'Min Temp (°C)': daily_api['temperature_2m_min'],
                })

                fig = go.Figure()
                fig.add_trace(go.Scatter(
                    x=df_chart['Date'],
                    y=df_chart['Max Temp (°C)'],
                    name='Max Temp',
                    line=dict(color='tomato', width=2)
                ))
                fig.add_trace(go.Scatter(
                    x=df_chart['Date'],
                    y=df_chart['Min Temp (°C)'],
                    name='Min Temp',
                    line=dict(color='steelblue', width=2),
                    fill='tonexty',
                    fillcolor='rgba(70,130,180,0.1)'
                ))
                fig.add_vline(
                    x=pd.Timestamp(str(target_date)).timestamp() * 1000,
                    line_dash="dash",
                    line_color="yellow",
                    annotation_text="Selected date"
                )
                fig.update_layout(
                    xaxis_title='Date',
                    yaxis_title='Temperature (°C)',
                    hovermode='x unified',
                    height=350,
                    plot_bgcolor='rgba(0,0,0,0)',
                    paper_bgcolor='rgba(0,0,0,0)'
                )
                st.plotly_chart(fig, use_container_width=True)

                st.caption("Source: Open-Meteo API — real atmospheric forecast data updated hourly.")

            else:
                st.error("Date not available in forecast. Try a closer date.")

        else:
            st.error("City not found. Try a different spelling.")

    except Exception as e:
        st.error(f"Error: {e}")

