import streamlit as st
import pandas as pd
import folium
from streamlit_folium import st_folium
import requests

# Загружаем данные (без модели!)
df = pd.read_csv('covid_19_clean_complete.csv')
df['Date'] = pd.to_datetime(df['Date'])
df_countries = df.groupby('Country/Region').agg({
    'Lat':'mean', 'Long':'mean', 'Confirmed':'max'
}).reset_index()

st.title("COVID-19 ML-прогноз: новые случаи по странам и датам (API)")
country = st.selectbox("Страна", df_countries['Country/Region'].sort_values())
default_confirmed = int(df_countries[df_countries['Country/Region'] == country]['Confirmed'])
lat = float(df_countries[df_countries['Country/Region'] == country]['Lat'])
lon = float(df_countries[df_countries['Country/Region'] == country]['Long'])

col1, col2 = st.columns(2)
with col1:
    date = st.date_input("Дата прогноза", pd.Timestamp("2022-07-01"))
with col2:
    confirmed = st.number_input("Текущее Confirmed (можно скорректировать)", min_value=0, value=default_confirmed)

# --- API endpoint ---
API_URL = "http://159.223.232.177:8000/predict"  # Если разносишь по разным машинам — укажи нужный адрес

if st.button("Предсказать и показать на карте"):
    # Готовим данные для API
    payload = {
        "country": country,
        "confirmed": int(confirmed),
        "lat": lat,
        "lon": lon,
        "date": str(date)
    }
    try:
        response = requests.post(API_URL, json=payload, timeout=10)
        if response.status_code == 200:
            result = response.json()
            predicted_new_cases = int(result["predicted_new_cases"])
            st.success(f"Прогноз новых случаев в {country} на {date}: {predicted_new_cases}")
        else:
            st.error(f"Ошибка {response.status_code}: {response.text}")
            predicted_new_cases = 0
    except Exception as e:
        st.error(f"Ошибка при обращении к API: {e}")
        predicted_new_cases = 0

    # Карта
    m = folium.Map(location=[lat, lon], zoom_start=4, tiles='CartoDB dark_matter')
    folium.CircleMarker(
        location=[lat, lon],
        radius=max(4, min(20, predicted_new_cases//100)),
        color='red',
        fill=True,
        fill_opacity=0.6,
        popup=f"{country}: {predicted_new_cases} новых случаев"
    ).add_to(m)
    st_folium(m, width=700, height=500)
