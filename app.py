import streamlit as st
import pandas as pd
import joblib
import folium
from streamlit_folium import st_folium

# Загружаем модель и данные
model = joblib.load('model.pkl')
df = pd.read_csv('covid_19_clean_complete.csv')
df['Date'] = pd.to_datetime(df['Date'])
df_countries = df.groupby('Country/Region').agg({
    'Lat':'mean', 'Long':'mean', 'Confirmed':'max'
}).reset_index()

st.title("COVID-19 ML-прогноз: новые случаи по странам и датам")
country = st.selectbox("Страна", df_countries['Country/Region'].sort_values())
default_confirmed = int(df_countries[df_countries['Country/Region'] == country]['Confirmed'])
lat = float(df_countries[df_countries['Country/Region'] == country]['Lat'])
lon = float(df_countries[df_countries['Country/Region'] == country]['Long'])

col1, col2 = st.columns(2)
with col1:
    date = st.date_input("Дата прогноза", pd.Timestamp("2022-07-01"))
with col2:
    confirmed = st.number_input("Текущее Confirmed (можно скорректировать)", min_value=0, value=default_confirmed)

if st.button("Предсказать и показать на карте"):
    dayofweek = pd.to_datetime(date).dayofweek
    month = pd.to_datetime(date).month
    X = [[lat, lon, confirmed, dayofweek, month]]
    predicted_new_cases = int(model.predict(X)[0])

    st.success(f"Прогноз новых случаев в {country} на {date}: {predicted_new_cases}")

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

