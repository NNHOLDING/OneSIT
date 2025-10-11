import streamlit as st
import pandas as pd
from datetime import datetime
import pytz
from math import radians, cos, sin, asin, sqrt
from streamlit_geolocation import geolocation

cr_timezone = pytz.timezone("America/Costa_Rica")

# 📍 Coordenadas del punto de control
LAT_CENTRO = 9.99413016099283
LON_CENTRO = -84.23354393628277
RADIO_METROS = 30

# 📏 Función Haversine para calcular distancia entre dos puntos
def esta_dentro_del_radio(lat1, lon1, lat2, lon2, radio_metros=30):
    lat1, lon1, lat2, lon2 = map(radians, [lat1, lon1, lat2, lon2])
    dlat = lat2 - lat1
    dlon = lon2 - lon1
    a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
    c = 2 * asin(sqrt(a))
    distancia = 6371000 * c  # Radio de la Tierra en metros
    return distancia <= radio_metros

# 🗃️ Función para cargar datos desde la hoja "Jornadas"
def cargar_datos(conectar_funcion):
    hoja = conectar_funcion().worksheet("Jornadas")
    datos = hoja.get_all_values()
    df = pd.DataFrame(datos[1:], columns=datos[0])
    return df

# ➕ Función para agregar inicio de jornada
def agregar_fila_inicio(conectar_funcion, fecha, usuario, bodega, hora):
    hoja = conectar_funcion().worksheet("Jornadas")
    nueva_fila = [fecha, usuario, bodega, hora, "", "", "", "", ""]
    hoja.append_row(nueva_fila)

# ✅ Función para actualizar fecha de cierre
def actualizar_fecha_cierre(conectar_funcion, fecha, usuario, bodega, hora):
    hoja = conectar_funcion().worksheet("Jornadas")
    datos = hoja.get_all_values()
    for i, fila in enumerate(datos[1:], start=2):  # saltar encabezado
        if (
            fila[0] == fecha and
            fila[1] == usuario and
            fila[2] == bodega and
            fila[4] == ""  # fecha cierre vacío
        ):
            hoja.update_cell(i, 5, hora)  # columna 5 = fecha cierre
            return True
    return False

# 🎛️ Panel de gestión de jornada
def gestionar_jornada(conectar_funcion, usuario_actual):
    st.title("📝 Gestión de Jornada")

    now_cr = datetime.now(cr_timezone)
    fecha_actual = now_cr.strftime("%Y-%m-%d")
    hora_actual = now_cr.strftime("%H:%M:%S")

    st.text_input("Usuario", value=usuario_actual, disabled=True)
    st.text_input("Fecha", value=fecha_actual, disabled=True)

    bodegas = [
        "Bodega Barrio Cuba", "CEDI Coyol", "Bodega Cañas",
        "Bodega Coto", "Bodega San Carlos", "Bodega Pérez Zeledón"
    ]
    bodega = st.selectbox("Selecciona la bodega", bodegas)

    datos = cargar_datos(conectar_funcion)

    registro_existente = datos[
        (datos["usuario"] == usuario_actual) &
        (datos["fecha"] == fecha_actual) &
        (datos["Bodega"] == bodega)
    ]

    # 📍 Captura automática de ubicación
    st.subheader("📍 Verificación de ubicación automática")
    ubicacion = geolocation()

    if ubicacion and "coords" in ubicacion:
        lat_usuario = ubicacion["coords"]["latitude"]
        lon_usuario = ubicacion["coords"]["longitude"]
        st.success(f"Ubicación detectada: {lat_usuario:.6f}, {lon_usuario:.6f}")
    else:
        st.error("❌ No se pudo validar tu ubicación. Asegúrate de permitir el acceso en el navegador y recarga la página.")
        lat_usuario = None
        lon_usuario = None

    col1, col2 = st.columns(2)
    with col1:
        if st.button("📌 Iniciar jornada"):
            if not bodega.strip():
                st.warning("Debes seleccionar una bodega.")
            elif not registro_existente.empty:
                st.warning("Ya registraste el inicio de jornada para hoy.")
            elif lat_usuario is None or lon_usuario is None:
                st.error("❌ No se pudo validar tu ubicación.")
            elif not esta_dentro_del_radio(lat_usuario, lon_usuario, LAT_CENTRO, LON_CENTRO, RADIO_METROS):
                st.error("❌ Estás fuera del rango permitido para registrar la jornada.")
            else:
                agregar_fila_inicio(conectar_funcion, fecha_actual, usuario_actual, bodega, hora_actual)
                st.success(f"✅ Inicio registrado a las {hora_actual}")

    with col2:
        if st.button("✅ Cerrar jornada"):
            if registro_existente.empty:
                st.warning("Debes iniciar jornada antes de cerrarla.")
            elif registro_existente.iloc[0].get("fecha cierre", "") != "":
                st.warning("Ya has cerrado la jornada de hoy.")
            else:
                if actualizar_fecha_cierre(conectar_funcion, fecha_actual, usuario_actual, bodega, hora_actual):
                    st.success(f"✅ Jornada cerrada correctamente a las {hora_actual}")
                else:
                    st.error("❌ No se pudo registrar el cierre.")
