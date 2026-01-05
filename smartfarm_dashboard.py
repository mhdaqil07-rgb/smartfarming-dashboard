import streamlit as st
import requests

st.set_page_config(page_title="Smart Farming Dashboard")

st.title("🌱 Smart Farming Dashboard")
st.caption("Monitoring Suhu & Kelembaban (ESP32 → Firebase)")

FIREBASE_URL = "https://dhtttt-17fe2-default-rtdb.firebaseio.com/smartfarm/dht11.json"

response = requests.get(FIREBASE_URL, timeout=10)
data = response.json()

if data:
    col1, col2 = st.columns(2)

    with col1:
        st.metric(
            "🌡️ Suhu (°C)",
            float(data["temperature"]),
            key=f"suhu_{data['timestamp']}"
        )

    with col2:
        st.metric(
            "💧 Kelembaban (%)",
            float(data["humidity"]),
            key=f"hum_{data['timestamp']}"
        )

    st.caption(f"Last update: {data['timestamp']}")
else:
    st.warning("Data belum tersedia")
