import streamlit as st
import firebase_admin
from firebase_admin import credentials, db

st.title("Smart Farming Dashboard 🌱")
st.subheader("Realtime DHT11 Monitoring (ESP32 → Firebase)")

# Init Firebase (hindari double init)
if not firebase_admin._apps:
    cred = credentials.Certificate("serviceAccount.json")
    firebase_admin.initialize_app(cred, {
        "databaseURL": "https://dhtttt-17fe2-default-rtdb.firebaseio.com/"
    })

# Baca data
ref = db.reference("/DHT11")
data = ref.get()

if data:
    st.metric("🌡 Suhu (°C)", data.get("temperature"))
    st.metric("💧 Kelembaban (%)", data.get("humidity"))
else:
    st.warning("Belum ada data dari ESP32!")
import time
time.sleep(3)
st.rerun()

