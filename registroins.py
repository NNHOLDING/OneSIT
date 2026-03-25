import streamlit as st
import datetime
import pytz
import gspread
from google.oauth2.service_account import Credentials
from streamlit_time_picker import st_time_picker

cr_timezone = pytz.timezone("America/Costa_Rica")

def panel_registro():
    st.title("🕒 Registro INS con picker dinámico")

    # Estilo oscuro para el picker
    st.markdown(
        """
        <style>
        .stTimePicker input {
            background-color: #000000 !important;
            color: #FFFFFF !important;
            font-size: 18px !important;
            text-align: center;
        }
        .stTimePicker label {
            color: #FFFFFF !important;
        }
        </style>
        """,
        unsafe_allow_html=True
    )

    ahora = datetime.datetime.now(cr_timezone)

    # Picker dinámico de hora en un solo campo
    hora = st_time_picker("Hora", value=ahora.time())

    # Otros campos
    fecha = st.date_input("Fecha", ahora.date())
    numero_evento = st.text_input("Número de evento")

    # Conexión con Google Sheets
    scope = ["https://spreadsheets.google.com/feeds",
             "https://www.googleapis.com/auth/drive"]
    creds = Credentials.from_service_account_info(st.secrets["gcp_service_account"], scopes=scope)
    client = gspread.authorize(creds)
    sheet = client.open_by_key("1PtUtGidnJkZZKW5CW4IzMkZ1tFk9dJLrGKe9vMwg0N0").worksheet("INS")

    # Botón de guardar
    if st.button("Guardar"):
        sheet.append_row([
            str(fecha),
            hora.strftime("%H:%M"),
            numero_evento,
            st.session_state.get("nombre_empleado", "Sistema")
        ])
        st.success("✅ La información fue almacenada exitosamente")
