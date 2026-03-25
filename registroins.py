import streamlit as st
import datetime
import pytz
import matplotlib.pyplot as plt
import numpy as np
import gspread
from google.oauth2.service_account import Credentials

cr_timezone = pytz.timezone("America/Costa_Rica")

def dibujar_reloj(hora_actual):
    fig, ax = plt.subplots(figsize=(3,3))
    ax.set_facecolor("black")
    ax.axis("off")

    # Círculo del reloj
    circle = plt.Circle((0,0), 1, fill=False, color="white", linewidth=2)
    ax.add_artist(circle)

    # Hora actual
    horas = hora_actual.hour % 12
    minutos = hora_actual.minute
    segundos = hora_actual.second

    # Ángulos de las manecillas
    ang_h = np.pi/2 - (2*np.pi/12)*horas - (2*np.pi/12)*(minutos/60)
    ang_m = np.pi/2 - (2*np.pi/60)*minutos
    ang_s = np.pi/2 - (2*np.pi/60)*segundos

    # Manecillas
    ax.plot([0, np.cos(ang_h)*0.5], [0, np.sin(ang_h)*0.5], color="white", linewidth=3)
    ax.plot([0, np.cos(ang_m)*0.8], [0, np.sin(ang_m)*0.8], color="white", linewidth=2)
    ax.plot([0, np.cos(ang_s)*0.9], [0, np.sin(ang_s)*0.9], color="red", linewidth=1)

    ax.set_xlim(-1.1,1.1)
    ax.set_ylim(-1.1,1.1)
    return fig

def panel_registro():
    st.title("🕒 Registro INS con reloj analógico")

    # Hora actual
    hora_actual = datetime.datetime.now(cr_timezone)

    # Mostrar reloj gráfico
    fig = dibujar_reloj(hora_actual)
    st.pyplot(fig)

    # Inputs adicionales
    fecha = st.date_input("Fecha", hora_actual.date())
    numero_evento = st.text_input("Número de evento")

    # Mostrar hora actual en texto también
    st.write(f"Hora actual: {hora_actual.strftime('%H:%M:%S')}")

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
            hora_actual.strftime("%H:%M:%S"),
            numero_evento,
            st.session_state.get("nombre_empleado", "Sistema")
        ])
        st.success("✅ La información fue almacenada exitosamente")