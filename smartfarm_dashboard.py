import streamlit as st
import requests

st.set_page_config(page_title="Smart Farming Dashboard")

st.title("🌱 Smart Farming Dashboard")
st.caption("Monitoring Suhu & Kelembaban (ESP32 → Firebase)")

FIREBASE_URL = "https://dhtttt-17fe2-default-rtdb.firebaseio.com/smartfarm/dht11.json"

if st.button("🔄 Refresh Data"):
    st.rerun()

response = requests.get(FIREBASE_URL, timeout=10)
data = response.json()

if data:
    col1, col2 = st.columns(2)

    with col1:
        st.metric(
            "🌡️ Suhu (°C)",
            float(data.get("temperature", 0))
        )

    with col2:
        st.metric(
            "💧 Kelembaban (%)",
            float(data.get("humidity", 0))
        )

    st.success("Data berhasil ditampilkan")
else:
    st.warning("Data belum tersedia di Firebase")
