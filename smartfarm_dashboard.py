import streamlit as st
import firebase_admin
from firebase_admin import credentials, db

st.title("Smart Farming Dashboard 🌱")
st.subheader("Realtime DHT11 Monitoring")

if not firebase_admin._apps:
    firebase_config = dict(st.secrets["firebase"])
    cred = credentials.Certificate(firebase_config)
    firebase_admin.initialize_app(cred, {
        "databaseURL": "https://dhtttt-17fe2-default-rtdb.firebaseio.com"
    })

ref = db.reference("smartfarm/dht11")
data = ref.get()

if data:
    st.metric("Temperature (°C)", data.get("temperature"))
    st.metric("Humidity (%)", data.get("humidity"))
else:
    st.warning("Belum ada data dari ESP32")
