# registroins.py
import streamlit as st
import pytz
import datetime
import gspread
from google.oauth2.service_account import Credentials
from geopy.geocoders import Nominatim

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

    # Obtener coordenadas desde el navegador con JS
    coords = st.experimental_get_query_params()
    lat = coords.get("lat", [None])[0]
    lon = coords.get("lon", [None])[0]

    provincia, canton, distrito = "", "", ""
    if lat and lon:
        geolocator = Nominatim(user_agent="geoapi")
        loc = geolocator.reverse(f"{lat}, {lon}")
        if loc:
            address = loc.raw.get("address", {})
            provincia = address.get("province", address.get("state", ""))
            canton = address.get("municipality", address.get("county", ""))
            distrito = address.get("neighbourhood", address.get("suburb", ""))

    st.markdown("""
        <script>
        navigator.geolocation.getCurrentPosition(
            (pos) => {
                const lat = pos.coords.latitude;
                const lon = pos.coords.longitude;
                const query = new URLSearchParams(window.location.search);
                query.set("lat", lat);
                query.set("lon", lon);
                window.location.search = query.toString();
            }
        );
        </script>
    """, unsafe_allow_html=True)

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