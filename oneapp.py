import streamlit as st
import pandas as pd
from datetime import datetime
import pytz
import requests
from PIL import Image
from io import BytesIO

from auth import validar_login
from google_sheets import conectar_sit_hh
from registro import registrar_handheld  # ← nuevo import desde módulo separado

# 🌎 Zona horaria
cr_timezone = pytz.timezone("America/Costa_Rica")

# 📊 Cargar registros desde hoja "HH"
def cargar_handhelds():
    hoja = conectar_sit_hh().worksheet("HH")
    datos = hoja.get_all_values()
    df = pd.DataFrame(datos[1:], columns=datos[0])
    df["Fecha"] = pd.to_datetime(df["Fecha"], errors="coerce")
    return df

# 🧼 Inicializar sesión
for key in ["logueado_handheld", "rol_handheld", "nombre_empleado", "codigo_empleado"]:
    if key not in st.session_state:
        st.session_state[key] = ""

# 👋 Mensaje al salir
if st.query_params.get("salida") == "true":
    for key in ["logueado_handheld", "rol_handheld", "nombre_empleado", "codigo_empleado"]:
        st.session_state[key] = ""
    st.success("👋 ¡Hasta pronto!")

# 🖼️ Mostrar logo en login
if not st.session_state.logueado_handheld:
    url_logo = "https://drive.google.com/uc?export=view&id=1YzqBlolo6MZ8JYzUJVvr7LFvTPP5WpM2"
    response = requests.get(url_logo)

    if response.status_code == 200:
        image = Image.open(BytesIO(response.content))
        st.image(image, use_container_width=True)
    else:
        st.warning("⚠️ No se pudo cargar el logo.")
