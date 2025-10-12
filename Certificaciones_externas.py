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

    hora_actual_crc = datetime.now(cr_timezone).strftime("%H:%M")
    hora_inicio = streamlit_js_eval(
        js_expressions=f"""
        new Promise((resolve, reject) => {{
            const input = document.createElement("input");
            input.type = "text";
            input.id = "hora_inicio";
            input.placeholder = "Hora de inicio";
            input.style = "padding:8px; font-size:16px; width:200px; margin-bottom:10px;";
            document.body.appendChild(input);

            const script = document.createElement("script");
            script.src = "https://cdn.jsdelivr.net/npm/flatpickr";
            script.onload = () => {{
                flatpickr("#hora_inicio", {{
                    enableTime: true,
                    noCalendar: true,
                    dateFormat: "H:i",
                    time_24hr: true,
                    defaultDate: "{hora_actual_crc}",
                    onChange: function(selectedDates, dateStr, instance) {{
                        resolve(dateStr);
                    }}
                }});
            }};
            document.body.appendChild(script);
        }})
        """,
        key="hora_inicio_reloj"
    )

    hora_fin = streamlit_js_eval(
        js_expressions=f"""
        new Promise((resolve, reject) => {{
            const input = document.createElement("input");
            input.type = "text";
            input.id = "hora_fin";
            input.placeholder = "Hora de cierre";
            input.style = "padding:8px; font-size:16px; width:200px; margin-bottom:10px;";
            document.body.appendChild(input);

            const script = document.createElement("script");
            script.src = "https://cdn.jsdelivr.net/npm/flatpickr";
            script.onload = () => {{
                flatpickr("#hora_fin", {{
                    enableTime: true,
                    noCalendar: true,
                    dateFormat: "H:i",
                    time_24hr: true,
                    defaultDate: "{hora_actual_crc}",
                    onChange: function(selectedDates, dateStr, instance) {{
                        resolve(dateStr);
                    }}
                }});
            }};
            document.body.appendChild(script);
        }})
        """,
        key="hora_fin_reloj"
    )

    if st.button("📥 Enviar Certificación"):
        try:
            formato = "%H:%M"
            inicio_dt = datetime.strptime(hora_inicio, formato)
            fin_dt = datetime.strptime(hora_fin, formato)
            duracion = int((fin_dt - inicio_dt).total_seconds() / 60)
            if duracion < 0:
                st.error("⚠️ La hora de fin no puede ser anterior a la hora de inicio.")
            else:
                hora_registro = datetime.now(cr_timezone).strftime("%H:%M:%S")
                site = "Dispositivo externo"
                hoja = conectar_funcion().worksheet("TCertificaciones")
                hoja.append_row([
                    fecha_cert, ruta, certificador, persona_conteo,
                    hora_inicio, hora_fin,
                    duracion, hora_registro, site
                ])
                st.success("✅ Certificación enviada correctamente.")
        except Exception as e:
            st.error(f"❌ Error al enviar certificación: {e}")
