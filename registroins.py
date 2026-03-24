# registroins.py
import streamlit as st
import pytz
import datetime
import gspread
from google.oauth2.service_account import Credentials
from geopy.geocoders import Nominatim
from streamlit_js_eval import streamlit_js_eval

# Configuración de zona horaria
cr_timezone = pytz.timezone("America/Costa_Rica")

def panel_registro():
    # Conexión con Google Sheets usando st.secrets
    scope = ["https://spreadsheets.google.com/feeds",
             "https://www.googleapis.com/auth/drive"]

    creds = Credentials.from_service_account_info(st.secrets["gcp_service_account"], scopes=scope)
    client = gspread.authorize(creds)
    sheet = client.open_by_key("1PtUtGidnJkZZKW5CW4IzMkZ1tFk9dJLrGKe9vMwg0N0").worksheet("INS")

    st.title("📝 Registro INS")

    fecha = st.date_input("Fecha", datetime.datetime.now(cr_timezone).date())
    hora = st.time_input("Hora", datetime.datetime.now(cr_timezone).time())
    numero_evento = st.text_input("Número de evento")

    # Obtener coordenadas reales del dispositivo vía JS
    lat = streamlit_js_eval(js_expressions="navigator.geolocation.getCurrentPosition(pos => pos.coords.latitude)", key="lat")
    lon = streamlit_js_eval(js_expressions="navigator.geolocation.getCurrentPosition(pos => pos.coords.longitude)", key="lon")

    provincia, canton, distrito = "", "", ""
    if lat and lon:
        geolocator = Nominatim(user_agent="geoapi")
        loc = geolocator.reverse(f"{lat}, {lon}")
        if loc:
            address = loc.raw.get("address", {})
            provincia = address.get("province", address.get("state", ""))
            canton = address.get("municipality", address.get("county", ""))
            distrito = address.get("neighbourhood", address.get("suburb", ""))

        st.write(f"📍 Coordenadas detectadas: {lat}, {lon}")

    if st.button("Guardar"):
        sheet.append_row([
            str(fecha),
            str(hora),
            numero_evento,
            lat,
            lon,
            provincia,
            canton,
            distrito,
            st.session_state.get("nombre_empleado", "Sistema"),
            f"{lat},{lon}" if lat and lon else ""
        ])
        st.success("✅ La información fue almacenada exitosamente")