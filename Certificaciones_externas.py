import streamlit as st
from datetime import datetime
from pytz import timezone
import gspread
from oauth2client.service_account import ServiceAccountCredentials

# Configuración de la página
st.set_page_config(
    page_title="HH HOLDING",
    page_icon="ttps://drive.google.com/uc?export=view&id=1P6OSXZMR4DI_cEgwjk1ZVJ6B8aLS1_qq" width="250",  # favicon personalizado
    layout="centered"
)

# Logo e identidad visual
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

# Zona horaria Costa Rica
cr_timezone = timezone("America/Costa_Rica")

# Conexión al libro de Google Sheets
def conectar_libro():
    scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
    creds = ServiceAccountCredentials.from_json_keyfile_dict(st.secrets["gcp_service_account"], scope)
    client = gspread.authorize(creds)
    return client.open_by_url("https://docs.google.com/spreadsheets/d/1PtUtGidnJkZZKW5CW4IzMkZ1tFk9dJLrGKe9vMwg0N0/edit")

# Obtener lista de usuarios desde hoja "usuarios"
def obtener_usuarios():
    hoja = conectar_libro().worksheet("usuarios")
    datos = hoja.get_all_values()
    return sorted([fila[1] for fila in datos[1:] if fila[1]])

# Formulario de certificación
st.title("📝 Certificacion de ruta Sigma")

fecha_actual = datetime.now(cr_timezone).strftime("%Y-%m-%d")
st.text_input("Fecha", value=fecha_actual, disabled=True)

ruta = st.selectbox("Ruta", ["100", "200", "300", "400", "500", "600", "700", "800", "otro"])
usuarios = obtener_usuarios()
certificador = st.selectbox("Certificador", usuarios)
persona_conteo = st.selectbox("Persona conteo", usuarios)

hora_actual_crc = datetime.now(cr_timezone).time().replace(second=0, microsecond=0)
hora_inicio = st.time_input("Hora inicio", value=hora_actual_crc)
hora_fin = st.time_input("Hora fin", value=hora_actual_crc)

if st.button("📥 Enviar Certificación"):
    campos = {
        "Ruta": ruta,
        "Certificador": certificador,
        "Persona conteo": persona_conteo,
        "Hora inicio": hora_inicio,
        "Hora fin": hora_fin
    }
    faltantes = [campo for campo, valor in campos.items() if not valor]
    if faltantes:
        st.warning(f"⚠️ Debes completar los siguientes campos: {', '.join(faltantes)}")
    else:
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

                hoja = conectar_libro().worksheet("TCertificaciones")
                hoja.append_row([
                    fecha_actual, ruta, certificador, persona_conteo,
                    hora_inicio.strftime(formato), hora_fin.strftime(formato),
                    duracion, hora_registro, site
                ])
                st.success("✅ Certificación enviada correctamente.")
        except Exception as e:

            st.error(f"❌ Error al enviar certificación: {e}")


