import streamlit as st
import firebase_admin
from firebase_admin import credentials, db
from streamlit_autorefresh import st_autorefresh

# ================== STREAMLIT UI ==================
st.set_page_config(page_title="Smart Farming Dashboard", layout="centered")
st.title("🌱 Smart Farming Dashboard")
st.subheader("Realtime DHT11 Monitoring")

# Auto refresh tiap 5 detik
st_autorefresh(interval=5000, key="refresh")

# ================== FIREBASE INIT ==================
if not firebase_admin._apps:
    firebase_config = dict(st.secrets["firebase"])

    # PERBAIKI PRIVATE KEY (\n -> newline asli)
    firebase_config["private_key"] = firebase_config["private_key"].replace("\\n", "\n")

    cred = credentials.Certificate(firebase_config)

    firebase_admin.initialize_app(cred, {
        "databaseURL": "https://dhtttt-17fe2-default-rtdb.firebaseio.com"
    })

# ================== AMBIL DATA ==================
ref = db.reference("smartfarm/dht11")
data = ref.get()

# ================== TAMPILKAN DATA ==================
if data:
    col1, col2 = st.columns(2)

    col1.metric("🌡️ Temperature (°C)", data.get("temperature", "-"))
    col2.metric("💧 Humidity (%)", data.get("humidity", "-"))
else:
    st.warning("Belum ada data dari ESP32")
