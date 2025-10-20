import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
import pytz
from math import radians, cos, sin, asin, sqrt
from streamlit_js_eval import streamlit_js_eval
import gspread
from oauth2client.service_account import ServiceAccountCredentials

import streamlit.components.v1 as components

st.set_page_config(
    page_title="Smart Intelligence Tools",
    page_icon="https://github.com/NNHOLDING/marcas_sit/raw/main/sitfavicon.ico",
    layout="centered"
)
# Configuración visual
st.set_page_config(page_title="SIT", page_icon="🏢", layout="centered")

# Logo y encabezado
url_logo = "https://drive.google.com/uc?export=view&id=1P6OSXZMR4DI_cEgwjk1ZVJ6B8aLS1_qq"
st.markdown(
    f"""
    <div style='text-align: center; margin-bottom: 20px;'>
        <img src="{url_logo}" width="200" />
        <h2 style='margin-top: 10px;'>SIGMA ALIMENTOS</h2>
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

    # Cargar rutas desde hoja TRutas
    def obtener_rutas():
        hoja_rutas = conectar_funcion().worksheet("TRutas")
        datos_rutas = hoja_rutas.get_all_values()
        df_rutas = pd.DataFrame(datos_rutas[1:], columns=datos_rutas[0])
        df_rutas.columns = df_rutas.columns.str.strip()
        return df_rutas

    df_rutas = obtener_rutas()
    rutas_disponibles = sorted(df_rutas["Numero ruta"].dropna().unique())
    ruta = st.selectbox("Ruta", rutas_disponibles, key="ruta_cert")

    # Cargar usuarios desde hoja usuarios
    def obtener_usuarios_df():
        hoja_usuarios = conectar_funcion().worksheet("usuarios")
        datos_usuarios = hoja_usuarios.get_all_values()
        df_usuarios = pd.DataFrame(datos_usuarios[1:], columns=datos_usuarios[0])
        df_usuarios.columns = df_usuarios.columns.str.strip()
        return df_usuarios

    df_usuarios = obtener_usuarios_df()
    usuarios = sorted(df_usuarios["nombreEmpleado"].dropna().unique())
    certificador = st.selectbox("Certificador", usuarios, key="certificador_cert")
    persona_conteo = st.selectbox("Persona conteo", usuarios, key="conteo_cert")

    # Campos ocultos: Tipo de ruta (Sección) y Empresa del certificador
    tipo_ruta = df_rutas[df_rutas["Numero ruta"] == ruta]["Seccion"].values[0] if ruta in df_rutas["Numero ruta"].values else ""
    empresa_certificador = df_usuarios[df_usuarios["nombreEmpleado"] == certificador]["Empresa"].values[0] if certificador in df_usuarios["nombreEmpleado"].values else ""

    hora_actual_crc = datetime.now(cr_timezone).time().replace(second=0, microsecond=0)
    hora_inicio = st.time_input("Hora inicio", value=hora_actual_crc, key="inicio_cert")
    hora_fin = st.time_input("Hora fin", value=hora_actual_crc, key="fin_cert")

    if st.button("📥 Enviar Certificación"):
        try:
            formato = "%H:%M"
            fecha_base = datetime.now(cr_timezone).date()

            # Combinar fecha base con hora de inicio y fin
            inicio_dt = datetime.combine(fecha_base, hora_inicio)
            fin_dt = datetime.combine(fecha_base, hora_fin)

            # Si la hora de fin es menor o igual, asumimos que es al día siguiente
            if fin_dt <= inicio_dt:
                fin_dt += timedelta(days=1)

            # Calcular duración en minutos
            duracion = int((fin_dt - inicio_dt).total_seconds() / 60)

            hora_registro = datetime.now(cr_timezone).strftime("%H:%M:%S")
            site = "Dispositivo externo"

            hoja = conectar_funcion().worksheet("TCertificaciones")
            hoja.append_row([
                fecha_cert, ruta, certificador, persona_conteo,
                hora_inicio.strftime(formato), hora_fin.strftime(formato),
                duracion, hora_registro, site,
                empresa_certificador,  # Columna J → Personal
                tipo_ruta              # Columna K → Tipo de ruta
            ])

            # Mostrar confirmación con duración en formato legible
            horas = duracion // 60
            minutos = duracion % 60
            duracion_legible = f"{horas} horas y {minutos} minutos" if horas else f"{minutos} minutos"
            st.success(f"✅ Certificación enviada correctamente. Duración registrada: {duracion_legible}.")
        except Exception as e:
            st.error(f"❌ Error al enviar certificación: {e}")


# 🧾 Footer institucional
st.markdown("""
    <hr style="margin-top: 50px; border: none; border-top: 1px solid #ccc;" />
    <div style="text-align: center; color: gray; font-size: 0.9em; margin-top: 20px;">
        Powered by NN HOLDING SOLUTIONS, Ever Be Better &copy; 2025, Todos los derechos reservados
    </div>
""", unsafe_allow_html=True)












