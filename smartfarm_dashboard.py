import streamlit as st
import requests

# ---------------- CONFIG ----------------
st.set_page_config(
    page_title="Smart Farming Dashboard",
    layout="centered"
)

FIREBASE_URL = "https://dhtttt-17fe2-default-rtdb.firebaseio.com/smartfarm/dht11.json"

# ---------------- UI ----------------
st.title("🌱 Smart Farming Dashboard")
st.caption("Monitoring Suhu & Kelembaban (ESP32 → Firebase)")

st.divider()

# Tombol refresh manual
if st.button("🔄 Ambil Data Terbaru"):
    st.experimental_set_query_params(refresh="1")

# ---------------- FETCH DATA ----------------
try:
    response = requests.get(FIREBASE_URL, timeout=10)

    if response.status_code == 200:
        data = response.json()

        if data:
            col1, col2 = st.columns(2)

            with col1:
                st.metric(
                    label="🌡️ Suhu (°C)",
                    value=f"{data.get('temperature', '-')} °C"
                )

            with col2:
                st.metric(
                    label="💧 Kelembaban (%)",
                    value=f"{data.get('humidity', '-')} %"
                )

            st.success("Data berhasil ditampilkan")
        else:
            st.warning("⚠️ Data belum tersedia di Firebase")

    else:
        st.error("❌ Gagal mengambil data dari Firebase")

except requests.exceptions.RequestException:
    st.error("🚫 Tidak dapat terhubung ke Firebase")

