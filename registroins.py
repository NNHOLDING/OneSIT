import streamlit as st
import pytz
import datetime
import gspread
from google.oauth2.service_account import Credentials
from geopy.geocoders import Nominatim
from streamlit_js_eval import streamlit_js_eval

cr_timezone = pytz.timezone("America/Costa_Rica")

def panel_registro():
    # Conexión con Google Sheets
    scope = ["https://spreadsheets.google.com/feeds",
             "https://www.googleapis.com/auth/drive"]
    creds = Credentials.from_service_account_info(st.secrets["gcp_service_account"], scopes=scope)
    client = gspread.authorize(creds)
    sheet = client.open_by_key("1PtUtGidnJkZZKW5CW4IzMkZ1tFk9dJLrGKe9vMwg0N0").worksheet("INS")

    st.title("📝 Registro INS")

    fecha = st.date_input("Fecha", datetime.datetime.now(cr_timezone).date())
    hora = st.time_input("Hora", datetime.datetime.now(cr_timezone).time())
    numero_evento = st.text_input("Número de evento")

    # Obtener coordenadas reales del dispositivo
    ubicacion = streamlit_js_eval(
        js_expressions="""
        new Promise((resolve, reject) => {
            navigator.geolocation.getCurrentPosition(
                (pos) => resolve({latitude: pos.coords.latitude, longitude: pos.coords.longitude}),
                (err) => reject(err)
            );
        })
        """,
        key="ubicacion"
    )

    lat, lon = None, None
    provincia, canton, distrito = "", "", ""
    if ubicacion and "latitude" in ubicacion and "longitude" in ubicacion:
        lat = ubicacion["latitude"]
        lon = ubicacion["longitude"]

        geolocator = Nominatim(user_agent="geoapi")
        loc = geolocator.reverse(f"{lat}, {lon}")
        if loc:
            address = loc.raw.get("address", {})
            provincia = address.get("province", address.get("state", ""))
            canton = address.get("municipality", address.get("county", ""))
            distrito = address.get("neighbourhood", address.get("suburb", ""))

        st.write(f"📍 Coordenadas detectadas: {lat}, {lon}")
        st.write(f"Provincia: {provincia}, Cantón: {canton}, Distrito: {distrito}")

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