import streamlit as st
import requests
from streamlit_autorefresh import st_autorefresh

# ---------------- CONFIG ----------------
st.set_page_config(page_title="Smart Farming Dashboard")

FIREBASE_URL = "https://dhtttt-17fe2-default-rtdb.firebaseio.com/smartfarm/dht11.json"

# ---------------- AUTO REFRESH ----------------
st_autorefresh(interval=5000, key="refresh")  # 5 detik

# ---------------- UI ----------------
st.title("🌱 Smart Farming Dashboard")
st.caption("Monitoring Suhu & Kelembaban (ESP32 → Firebase)")

# ---------------- FETCH DATA ----------------
try:
    response = requests.get(FIREBASE_URL, timeout=10)
    data = response.json()

    if data:
        col1, col2 = st.columns(2)

        with col1:
            st.metric(
                "🌡️ Suhu (°C)",
                f"{data.get('temperature', '-')} °C"
            )

        with col2:
            st.metric(
                "💧 Kelembaban (%)",
                f"{data.get('humidity', '-')} %"
            )

        st.success("Data realtime (auto refresh aktif)")
    else:
        st.warning("Data belum tersedia")

except Exception as e:
    st.error("Gagal mengambil data dari Firebase")
