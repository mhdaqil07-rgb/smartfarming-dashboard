import streamlit as st
import firebase_admin
from firebase_admin import credentials, db
from streamlit_autorefresh import st_autorefresh

# =========================
# PAGE CONFIG
# =========================
st.set_page_config(
    page_title="Smart Farming Dashboard",
    page_icon="🌱",
    layout="centered"
)

st.title("Smart Farming Dashboard 🌱")
st.subheader("Realtime DHT11 Monitoring")

# =========================
# AUTO REFRESH (5 detik)
# =========================
st_autorefresh(interval=5000, key="refresh")

# =========================
# FIREBASE INIT (SECRETS)
# =========================
if not firebase_admin._apps:
    cred = credentials.Certificate(st.secrets["firebase"])
    firebase_admin.initialize_app(cred, {
        "databaseURL": "https://dhtttt-17fe2-default-rtdb.firebaseio.com"
    })

# =========================
# READ DATA
# =========================
ref = db.reference("smartfarm/dht11")
data = ref.get()

# =========================
# DISPLAY DATA
# =========================
if data:
    col1, col2 = st.columns(2)

    with col1:
        st.metric("🌡️ Suhu (°C)", data.get("temperature", "-"))

    with col2:
        st.metric("💧 Kelembaban (%)", data.get("humidity", "-"))
else:
    st.warning("Belum ada data dari ESP32!")
