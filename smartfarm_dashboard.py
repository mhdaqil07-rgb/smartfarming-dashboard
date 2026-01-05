import streamlit as st
import requests
import pandas as pd
from datetime import datetime
import time

# ================= CONFIG =================
st.set_page_config(
    page_title="Smart Farming Dashboard",
    layout="wide"
)

FIREBASE_URL = "https://dhtttt-17fe2-default-rtdb.firebaseio.com/smartfarm/dht11.json"

REFRESH_INTERVAL = 5  # detik

# ================= INIT SESSION =================
if "history" not in st.session_state:
    st.session_state.history = pd.DataFrame(
        columns=["time", "temperature", "humidity"]
    )

if "last_update" not in st.session_state:
    st.session_state.last_update = 0

# ================= UI =================
st.title("🌱 Smart Farming Dashboard")
st.caption("Monitoring Suhu & Kelembaban (ESP32 → Firebase)")
st.info(f"Auto refresh setiap {REFRESH_INTERVAL} detik")

# ================= AUTO REFRESH LOGIC =================
current_time = time.time()

if current_time - st.session_state.last_update >= REFRESH_INTERVAL:
    try:
        response = requests.get(FIREBASE_URL, timeout=10)

        if response.status_code == 200:
            data = response.json()

            if data:
                temp = float(data.get("temperature", 0))
                hum = float(data.get("humidity", 0))
                now = datetime.now().strftime("%H:%M:%S")

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

                st.session_state.last_update = current_time

    except Exception as e:
        st.warning(f"Koneksi error: {e}")

# ================= METRIC =================
if not st.session_state.history.empty:
    latest = st.session_state.history.iloc[-1]

    col1, col2 = st.columns(2)
    col1.metric("🌡️ Suhu (°C)", f"{latest['temperature']}")
    col2.metric("💧 Kelembaban (%)", f"{latest['humidity']}")

# ================= GRAFIK =================
st.subheader("📈 Grafik Realtime")

if not st.session_state.history.empty:
    chart_df = st.session_state.history.set_index("time")
    st.line_chart(chart_df)

# ================= TABEL =================
st.subheader("📋 Histori Data")
st.dataframe(st.session_state.history, use_container_width=True)

# ================= AUTO RERUN HALUS =================
time.sleep(1)
st.rerun()
