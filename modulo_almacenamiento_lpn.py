import streamlit as st
import pandas as pd
from datetime import datetime
from exportar_ubicaciones import mostrar_opcion_exportar  # ✅ Nuevo módulo integrado

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

    try:
        col_registrado = hoja.find("Registrado por")
        if col_registrado:
            hoja.update_cell(fila + 2, col_registrado.col, usuario)
    except:
        pass

    try:
        col_fecha = hoja.find("Fecha de asignación")
        if col_fecha:
            hoja.update_cell(fila + 2, col_fecha.col, datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    except:
        pass

def actualizar_estado_lpn(libro, lpn):
    hoja = libro.worksheet("LPNs Generados")
    datos = hoja.get_all_values()
    encabezados = [col.strip() for col in datos[0]]
    df = pd.DataFrame(datos[1:], columns=encabezados)

    df["Número LPN"] = df["Número LPN"].str.strip().str.upper()
    lpn_normalizado = lpn.strip().upper()

    if "Número LPN" not in df.columns or "Estado" not in df.columns:
        st.warning("La hoja LPNs Generados no tiene las columnas necesarias.")
        return False

    fila = df[df["Número LPN"] == lpn_normalizado].index
    if fila.empty:
        st.warning(f"No se encontró el LPN {lpn_normalizado} en la hoja.")
        return False

    # Buscar columna 'Estado' de forma flexible
    encabezados_hoja = hoja.row_values(1)
    col_estado_idx = None
    for idx, nombre in enumerate(encabezados_hoja):
        if nombre.strip().lower() == "estado":
            col_estado_idx = idx + 1
            break

    if not col_estado_idx:
        st.warning("No se encontró la columna 'Estado' en la hoja LPNs Generados.")
        return False

    hoja.update_cell(fila[0] + 2, col_estado_idx, "No disponible")
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

    lpn = st.text_input("📄 Escanea o ingresa el LPN IB").strip().upper()
    ubicacion = st.text_input("📍 Escanea o ingresa la ubicación (ej. P01-1-1-1)").strip().upper()

    if st.button("📥 Almacenar"):
        if not lpn or not ubicacion:
            st.error("Debes ingresar el LPN y la ubicación.")
            return

        df_lpns["Número LPN"] = df_lpns["Número LPN"].str.strip().str.upper()
        lpn_row = df_lpns[df_lpns["Número LPN"] == lpn]
        if lpn_row.empty:
            st.error("El LPN no existe en la hoja LPNs Generados.")
            return
        if lpn_row.iloc[0]["Estado"].strip().lower() != "disponible":
            st.error("El LPN no está disponible para almacenamiento.")
            return

        df_ubicaciones["LPN Asignado"] = df_ubicaciones["LPN Asignado"].str.strip().str.upper()
        if lpn in df_ubicaciones["LPN Asignado"].values:
            st.error("Este LPN ya fue asignado a una ubicación.")
            return

        df_ubicaciones["codigo"] = df_ubicaciones.apply(
            lambda row: f"{str(row['Pasillo']).strip()}-{str(row['Tramo']).strip()}-{str(row['Nivel']).strip()}-{str(row['Posición']).strip()}",
            axis=1
        )
        df_ubicaciones["codigo"] = df_ubicaciones["codigo"].str.upper().str.strip()

        ubicacion_row = df_ubicaciones[df_ubicaciones["codigo"] == ubicacion]
        if ubicacion_row.empty:
            st.error("La ubicación no existe.")
            return

        if ubicacion_row.iloc[0]["Estado"].strip().lower() != "disponible":
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

    # ✅ Opción de exportar hoja de ubicaciones
    mostrar_opcion_exportar(libro)
