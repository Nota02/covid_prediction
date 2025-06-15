import streamlit as st
import pandas as pd
import folium
from streamlit_folium import st_folium
import requests

df = pd.read_csv('covid_19_clean_complete.csv')
df['Date'] = pd.to_datetime(df['Date'])
df_countries = df.groupby('Country/Region').agg({'Lat':'mean', 'Long':'mean'}).reset_index()

st.title("COVID-19 прогноз: новые случаи по странам и датам")

country = st.selectbox("Страна", df_countries['Country/Region'].sort_values())
lat = float(df_countries[df_countries['Country/Region'] == country]['Lat'].iloc[0])
lon = float(df_countries[df_countries['Country/Region'] == country]['Long'].iloc[0])

# Находим диапазон дат для страны
country_dates = df[df['Country/Region'] == country]['Date']
min_date, max_date = country_dates.min(), country_dates.max()

date = st.date_input(
    "Дата прогноза",
    value=max_date + pd.Timedelta(days=1),
    min_value=min_date,
    max_value=max_date + pd.Timedelta(days=60) 
)

API_URL = "http://localhost:8000/predict"

def get_confirmed_for_date(country, date):
    row = df[(df['Country/Region'] == country) & (df['Date'] == date)]
    if not row.empty:
        return int(row['Confirmed'].iloc[0])
    else:
        previous = df[(df['Country/Region'] == country) & (df['Date'] < date)].sort_values('Date')
        if not previous.empty:
            return int(previous['Confirmed'].iloc[-1])
        else:
            return 0

if 'prediction' not in st.session_state:
    st.session_state['prediction'] = None

if st.button("Предсказать и показать на карте"):
    selected_date = pd.to_datetime(date)

    last_known_date = df[df['Country/Region'] == country]['Date'].max()
    confirmed = get_confirmed_for_date(country, last_known_date)

    if selected_date <= last_known_date:
        confirmed = get_confirmed_for_date(country, selected_date)
        dayofweek = selected_date.dayofweek
        month = selected_date.month
        payload = {
            "country": country,
            "confirmed": confirmed,
            "lat": lat,
            "lon": lon,
            "date": str(selected_date.date())
        }
        response = requests.post(API_URL, json=payload, timeout=10)
        if response.status_code == 200:
            result = response.json()
            predicted_new_cases = int(result["predicted_new_cases"])
            st.session_state['prediction'] = {
                "country": country,
                "date": selected_date.date(),
                "predicted_new_cases": predicted_new_cases,
                "lat": lat,
                "lon": lon
            }
        else:
            st.error(f"Ошибка {response.status_code}: {response.text}")
            st.session_state['prediction'] = None

    else:
        horizon = (selected_date - last_known_date).days
        curr_confirmed = confirmed
        predicted_new_cases = 0
        for i in range(1, horizon + 1):
            pred_date = last_known_date + pd.Timedelta(days=i)
            payload = {
                "country": country,
                "confirmed": curr_confirmed,
                "lat": lat,
                "lon": lon,
                "date": str(pred_date.date())
            }
            response = requests.post(API_URL, json=payload, timeout=10)
            if response.status_code == 200:
                result = response.json()
                predicted_new_cases = max(0, int(result["predicted_new_cases"]))
                curr_confirmed += predicted_new_cases
            else:
                st.error(f"Ошибка {response.status_code}: {response.text}")
                predicted_new_cases = 0
                break
        st.session_state['prediction'] = {
            "country": country,
            "date": selected_date.date(),
            "predicted_new_cases": predicted_new_cases,
            "lat": lat,
            "lon": lon
        }

if st.session_state['prediction'] is not None:
    pred = st.session_state['prediction']
    st.success(f"Прогноз новых случаев в {pred['country']} на {pred['date']}: {pred['predicted_new_cases']}")
    m = folium.Map(location=[pred['lat'], pred['lon']], zoom_start=4, tiles='CartoDB dark_matter')
    folium.CircleMarker(
        location=[pred['lat'], pred['lon']],
        radius=max(4, min(20, pred['predicted_new_cases'] // 100)),
        color='red',
        fill=True,
        fill_opacity=0.6,
        popup=f"{pred['country']}: {pred['predicted_new_cases']} новых случаев"
    ).add_to(m)
    st_folium(m, width=700, height=500)
