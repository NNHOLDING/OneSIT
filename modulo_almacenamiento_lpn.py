import streamlit as st
import pandas as pd
from datetime import datetime

def cargar_hoja(libro, nombre_hoja):
    hoja = libro.worksheet(nombre_hoja)
    datos = hoja.get_all_values()
    if not datos or len(datos) < 2:
        return pd.DataFrame()
    encabezados = [col.strip() for col in datos[0]]
    return pd.DataFrame(datos[1:], columns=encabezados)

def actualizar_ubicacion(libro, fila, nuevo_estado, lpn, usuario):
    hoja = libro.worksheet("Ubicaciones")
    hoja.update_cell(fila + 2, hoja.find("Estado").col, nuevo_estado)
    hoja.update_cell(fila + 2, hoja.find("LPN Asignado").col, lpn)
    hoja.update_cell(fila + 2, hoja.find("Registrado por").col, usuario)
    hoja.update_cell(fila + 2, hoja.find("Fecha de asignación").col, datetime.now().strftime("%Y-%m-%d %H:%M:%S"))

def actualizar_estado_lpn(libro, lpn):
    hoja = libro.worksheet("LPNs Generados")
    datos = hoja.get_all_values()
    encabezados = [col.strip() for col in datos[0]]
    df = pd.DataFrame(datos[1:], columns=encabezados)
    if "Número LPN" not in df.columns or "Estado" not in df.columns:
        return False
    fila = df[df["Número LPN"] == lpn].index
    if fila.empty:
        return False
    hoja.update_cell(fila[0] + 2, hoja.find("Estado").col, "No disponible")
    return True

def mostrar_formulario_almacenamiento_lpn():
    st.subheader("📦 Almacenamiento de LPN IB")

    try:
        from google_sheets import conectar_sit_hh
        libro = st.session_state.get("libro_almacen_lpn")
        if not libro:
            libro = conectar_sit_hh()
            st.session_state.libro_almacen_lpn = libro
    except Exception as e:
        st.error(f"No se pudo conectar con Google Sheets: {e}")
        return

    df_ubicaciones = cargar_hoja(libro, "Ubicaciones")
    df_lpns = cargar_hoja(libro, "LPNs Generados")

    if df_ubicaciones.empty or df_lpns.empty:
        st.warning("Las hojas necesarias están vacías o mal formateadas.")
        return

    lpn = st.text_input("📄 Escanea o ingresa el LPN IB")
    ubicacion = st.text_input("📍 Escanea o ingresa la ubicación (ej. P01-1-1-1)")

    if st.button("📥 Almacenar"):
        if not lpn or not ubicacion:
            st.error("Debes ingresar el LPN y la ubicación.")
            return

        # Validar que el LPN esté disponible
        lpn_row = df_lpns[df_lpns["Número LPN"] == lpn]
        if lpn_row.empty or lpn_row.iloc[0]["Estado"].lower() != "disponible":
            st.error("El LPN no está disponible o no existe.")
            return

        # Buscar ubicación
        df_ubicaciones["codigo"] = df_ubicaciones.apply(
            lambda row: f"{row['Pasillo']}-{row['Tramo']}-{row['Nivel']}-{row['Posición']}", axis=1
        )
        ubicacion_row = df_ubicaciones[df_ubicaciones["codigo"] == ubicacion]

        if ubicacion_row.empty:
            st.error("La ubicación no existe.")
            return

        if ubicacion_row.iloc[0]["Estado"].lower() != "disponible":
            st.error("La ubicación está ocupada. No se puede almacenar aquí.")
            return

        fila_ubicacion = ubicacion_row.index[0]
        usuario = st.session_state.get("codigo_empleado", "Desconocido")
        actualizar_ubicacion(libro, fila_ubicacion, "Ocupado", lpn, usuario)
        actualizado = actualizar_estado_lpn(libro, lpn)

        if actualizado:
            st.success(f"LPN {lpn} almacenado exitosamente en {ubicacion}.")
        else:
            st.warning("La ubicación fue actualizada, pero no se pudo cambiar el estado del LPN.")
