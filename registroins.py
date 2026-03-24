# registroins.py
import streamlit as st
import pytz
import datetime
import gspread
from google.oauth2.service_account import Credentials
from geopy.geocoders import Nominatim
import geocoder

# Configuración de zona horaria
cr_timezone = pytz.timezone("America/Costa_Rica")

def panel_registro():
    # Conexión con Google Sheets usando st.secrets
    scope = ["https://spreadsheets.google.com/feeds",
             "https://www.googleapis.com/auth/drive"]

    creds = Credentials.from_service_account_info(st.secrets["gcp_service_account"], scopes=scope)
    client = gspread.authorize(creds)
    sheet = client.open_by_key("1PtUtGidnJkZZKW5CW4IzMkZ1tFk9dJLrGKe9vMwg0N0").worksheet("INS")

    # Geolocalización
    g = geocoder.ip("me")
    lat, lon = g.latlng if g.latlng else (None, None)

    # Reverse geocoding
    geolocator = Nominatim(user_agent="geoapi")
    location = geolocator.reverse(f"{lat}, {lon}") if lat and lon else None
    provincia, canton, distrito = ("", "", "")
    if location:
        address = location.raw.get("address", {})
        provincia = address.get("state", "")
        canton = address.get("county", "")
        distrito = address.get("suburb", "")

    # Interfaz Streamlit
    st.title("📝 Registro INS")

    fecha = st.date_input("Fecha", datetime.datetime.now(cr_timezone).date())
    hora = st.time_input("Hora", datetime.datetime.now(cr_timezone).time())
    numero_evento = st.text_input("Número de evento")

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
            f"{lat},{lon}"
        ])
        st.success("✅ La información fue almacenada exitosamente")