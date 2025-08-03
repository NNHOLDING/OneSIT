from datetime import datetime
import streamlit as st
from google_sheets import conectar_sit_hh
import pytz

# 🌎 Zona horaria
cr_timezone = pytz.timezone("America/Costa_Rica")

# 📋 Buscar fila existente en hoja "HH"
def buscar_fila(codigo, fecha):
    hoja = conectar_sit_hh().worksheet("HH")
    datos = hoja.get_all_values()
    for idx, fila in enumerate(datos[1:], start=2):
        if fila[1] == codigo and fila[0] == fecha:
            return idx, fila
    return None, None

# 📝 Registrar entrega o devolución en hoja "HH"
def registrar_handheld(codigo, nombre, equipo, tipo):
    hoja = conectar_sit_hh().worksheet("HH")
    fecha = datetime.now(cr_timezone).strftime("%Y-%m-%d")
    hora = datetime.now(cr_timezone).strftime("%H:%M:%S")
    fila_idx, fila = buscar_fila(codigo, fecha)

    if tipo == "entrega":
        if fila and fila[4]:
            st.warning("❌ Ya se registró una entrega para hoy.")
            return
        if fila:
            hoja.update_cell(fila_idx, 5, hora)
        else:
            hoja.append_row([fecha, codigo, Nombre, Equipo, hora, "", "Entregado"])
        st.success("✅ Entrega registrada correctamente.")
    elif tipo == "devolucion":
        if fila and fila[5]:
            st.warning("❌ Ya se registró una devolución para hoy.")
            return
        if fila:
            hoja.update_cell(fila_idx, 6, hora)
            hoja.update_cell(fila_idx, 7, "Devuelto")
        else:
            hoja.append_row([fecha, codigo, nombre, equipo, "", hora, "Devuelto"])

        st.success("✅ Devolución registrada correctamente.")
