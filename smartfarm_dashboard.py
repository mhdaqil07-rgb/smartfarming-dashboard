import streamlit as st
import firebase_admin
from firebase_admin import credentials, db

st.title("Smart Farming Dashboard 🌱")
st.write("Realtime DHT11 Monitoring")

# Cegah Firebase double init
if not firebase_admin._apps:
    cred = credentials.Certificate("serviceAccount.json")
    firebase_admin.initialize_app(cred, {
        "databaseURL": "https://dhtttt-17fe2-default-rtdb.firebaseio.com"
    })

ref = db.reference("smartfarm/dht11")
data = ref.get()

st.write("DEBUG DATA:", data)

if data:
    st.metric("🌡 Suhu (°C)", data.get("temperature"))
    st.metric("💧 Kelembaban (%)", data.get("humidity"))
else:
    st.warning("Belum ada data dari ESP32")
