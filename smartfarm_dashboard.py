import streamlit as st
import requests
import pandas as pd

st.set_page_config(page_title="Smart Farming Dashboard", layout="centered")

st.title("🌱 Smart Farming Dashboard")
st.caption("Monitoring Suhu & Kelembaban (ESP32 → Firebase)")

FIREBASE_URL = "https://dhtttt-17fe2-default-rtdb.firebaseio.com/smartfarm/dht11.json"

response = requests.get(FIREBASE_URL)

if response.status_code == 200:
    data = response.json()

    if data:
        # ubah JSON ke DataFrame
        df = pd.DataFrame.from_dict(data, orient="index")

        df.index.name = "timestamp"
        df.reset_index(inplace=True)

        # tampilkan nilai terbaru
        latest = df.iloc[-1]

        col1, col2 = st.columns(2)
        col1.metric("🌡️ Suhu (°C)", f"{latest['temperature']}")
        col2.metric("💧 Kelembaban (%)", f"{latest['humidity']}")

        st.subheader("📈 Grafik Suhu")
        st.line_chart(df.set_index("timestamp")["temperature"])

        st.subheader("📈 Grafik Kelembaban")
        st.line_chart(df.set_index("timestamp")["humidity"])

        with st.expander("📋 Histori Data"):
            st.dataframe(df)

    else:
        st.warning("Belum ada data di Firebase")
else:
    st.error("Gagal mengambil data dari Firebase")
