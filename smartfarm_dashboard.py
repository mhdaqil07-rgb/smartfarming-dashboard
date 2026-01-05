import streamlit as st
import requests
import pandas as pd
from datetime import datetime

# ================= CONFIG =================
st.set_page_config(
    page_title="Smart Farming Dashboard",
    layout="wide"
)

FIREBASE_URL = "https://dhtttt-17fe2-default-rtdb.firebaseio.com/smartfarm/dht11.json"

# ================= INIT SESSION =================
if "history" not in st.session_state:
    st.session_state.history = pd.DataFrame(
        columns=["time", "temperature", "humidity"]
    )

# ================= UI =================
st.title("🌱 Smart Farming Dashboard")
st.caption("Monitoring Suhu & Kelembaban (ESP32 → Firebase)")

# Tombol refresh manual
refresh = st.button("🔄 Ambil Data Terbaru")

# ================= FETCH DATA =================
try:
    response = requests.get(FIREBASE_URL, timeout=10)

    if response.status_code == 200:
        data = response.json()

        if data:
            temp = float(data.get("temperature", 0))
            hum = float(data.get("humidity", 0))
            now = datetime.now().strftime("%H:%M:%S")

            # Simpan histori
            new_row = {
                "time": now,
                "temperature": temp,
                "humidity": hum
            }

            st.session_state.history = pd.concat(
                [
                    st.session_state.history,
                    pd.DataFrame([new_row])
                ],
                ignore_index=True
            )

            # ================= METRIC =================
            col1, col2 = st.columns(2)
            col1.metric("🌡️ Suhu (°C)", f"{temp}")
            col2.metric("💧 Kelembaban (%)", f"{hum}")

        else:
            st.warning("Data kosong di Firebase")

    else:
        st.error("Gagal mengambil data dari Firebase")

except Exception as e:
    st.error(f"Koneksi error: {e}")

# ================= GRAFIK =================
st.subheader("📈 Grafik Realtime")

if not st.session_state.history.empty:
    chart_df = st.session_state.history.set_index("time")

    st.line_chart(chart_df)
else:
    st.info("Belum ada data histori")

# ================= TABEL =================
st.subheader("📋 Histori Data")
st.dataframe(st.session_state.history, use_container_width=True)
