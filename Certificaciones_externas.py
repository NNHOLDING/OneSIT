import streamlit as st
import pandas as pd
from datetime import datetime
import pytz
from math import radians, cos, sin, asin, sqrt
from streamlit_js_eval import streamlit_js_eval
import gspread
from oauth2client.service_account import ServiceAccountCredentials

# Configuración visual
st.set_page_config(page_title="HH HOLDING", page_icon="🏢", layout="centered")

# Logo y encabezado
url_logo = "https://drive.google.com/uc?export=view&id=1CgMBkG3rUwWOE9OodfBN1Tjinrl0vMOh"
st.markdown(
    f"""
    <div style='text-align: center; margin-bottom: 20px;'>
        <img src="{url_logo}" width="200" />
        <h2 style='margin-top: 10px;'>HH HOLDING</h2>
    </div>
    """,
    unsafe_allow_html=True
)

# Zona horaria
cr_timezone = pytz.timezone("America/Costa_Rica")

# Conexión al libro
def conectar_funcion():
    scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
    creds = ServiceAccountCredentials.from_json_keyfile_dict(st.secrets["gcp_service_account"], scope)
    client = gspread.authorize(creds)
    return client.open_by_url("https://docs.google.com/spreadsheets/d/1PtUtGidnJkZZKW5CW4IzMkZ1tFk9dJLrGKe9vMwg0N0/edit")

# Tabs
tab1, tab2 = st.tabs(["📥 Certificación", "📝 Gestión de Jornada"])

# 📥 Certificación
with tab1:
    st.subheader("Registro de certificación de ruta")

    fecha_cert = datetime.now(cr_timezone).strftime("%Y-%m-%d")
    st.text_input("Fecha", value=fecha_cert, disabled=True, key="fecha_cert")

    ruta = st.selectbox("Ruta", ["100", "200", "300", "400", "500", "600", "700", "800", "otro"], key="ruta_cert")

    def obtener_usuarios():
        hoja = conectar_funcion().worksheet("usuarios")
        datos = hoja.get_all_values()
        return sorted([fila[1] for fila in datos[1:] if fila[1]])

    usuarios = obtener_usuarios()
    certificador = st.selectbox("Certificador", usuarios, key="certificador_cert")
    persona_conteo = st.selectbox("Persona conteo", usuarios, key="conteo_cert")

    hora_actual_crc = datetime.now(cr_timezone).time().replace(second=0, microsecond=0)
    hora_inicio = st.time_input("Hora inicio", value=hora_actual_crc, key="inicio_cert")
    hora_fin = st.time_input("Hora fin", value=hora_actual_crc, key="fin_cert")

    if st.button("📥 Enviar Certificación"):
        try:
            formato = "%H:%M"
            inicio_dt = datetime.strptime(hora_inicio.strftime(formato), formato)
            fin_dt = datetime.strptime(hora_fin.strftime(formato), formato)
            duracion = int((fin_dt - inicio_dt).total_seconds() / 60)
            if duracion < 0:
                st.error("⚠️ La hora de fin no puede ser anterior a la hora de inicio.")
            else:
                hora_registro = datetime.now(cr_timezone).strftime("%H:%M:%S")
                site = "Dispositivo externo"
                hoja = conectar_funcion().worksheet("TCertificaciones")
                hoja.append_row([
                    fecha_cert, ruta, certificador, persona_conteo,
                    hora_inicio.strftime(formato), hora_fin.strftime(formato),
                    duracion, hora_registro, site
                ])
                st.success("✅ Certificación enviada correctamente.")
        except Exception as e:
            st.error(f"❌ Error al enviar certificación: {e}")

# 📝 Gestión de Jornada
with tab2:
    st.subheader("Gestión de jornada")

    # 🕒 Reloj visual interactivo
    components.html("""
    <div style="text-align:center; font-family:sans-serif;">
      <h4>🕒 Selecciona la hora</h4>
      <input type="range" id="hour" min="0" max="23" value="12" style="width:200px;">
      <label for="hour">Hora: <span id="hourVal">12</span></label><br><br>
      <input type="range" id="minute" min="0" max="59" value="30" style="width:200px;">
      <label for="minute">Minuto: <span id="minuteVal">30</span></label><br><br>
      <button onclick="setTime()">Establecer hora</button>
      <p id="selectedTime" style="margin-top:10px; font-weight:bold;"></p>
    </div>

    <script>
      const hourSlider = document.getElementById("hour");
      const minuteSlider = document.getElementById("minute");
      const hourVal = document.getElementById("hourVal");
      const minuteVal = document.getElementById("minuteVal");
      const selectedTime = document.getElementById("selectedTime");

      hourSlider.oninput = () => hourVal.textContent = hourSlider.value;
      minuteSlider.oninput = () => minuteVal.textContent = minuteSlider.value;

      function setTime() {
        const h = hourSlider.value.padStart(2, '0');
        const m = minuteSlider.value.padStart(2, '0');
        selectedTime.textContent = `Hora seleccionada: ${h}:${m}`;
      }
    </script>
    """, height=300)

    # Aquí continúa tu lógica de jornada...



