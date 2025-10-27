import streamlit as st
import pandas as pd
from datetime import datetime

def obtener_ultimo_consecutivo(libro, tipo_etiqueta, bodega):
    hoja = libro.worksheet("LPNs Generados")
    datos = hoja.get_all_values()
    df = pd.DataFrame(datos[1:], columns=datos[0])

    prefijo = "IB" if tipo_etiqueta == "Etiquetas IB" else "OB"
    base = f"{prefijo}{bodega}506"

    df_filtrada = df[df["Número LPN"].str.startswith(base)]
    if df_filtrada.empty:
        return 0
    ultimos = df_filtrada["Número LPN"].apply(lambda x: int(x[-5:]))
    return ultimos.max()

def generate_lpns(cantidad, usuario, bodega, tipo_etiqueta, libro):
    pais_codigo = "506"
    fecha_actual = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    estado = "disponible"
    lpns = []

    prefijo = "IB" if tipo_etiqueta == "Etiquetas IB" else "OB"
    base = f"{prefijo}{bodega}{pais_codigo}"

    consecutivo_inicial = obtener_ultimo_consecutivo(libro, tipo_etiqueta, bodega) + 1

    for i in range(cantidad):
        consecutivo = str(consecutivo_inicial + i).zfill(5)
        numero_lpn = f"{base}{consecutivo}"
        lpns.append([numero_lpn, fecha_actual, usuario, estado, bodega])

    hoja = libro.worksheet("LPNs Generados")
    hoja.append_rows(lpns)
    return lpns

def mostrar_formulario_lpn():
    st.subheader("🏷️ Generar LPNs")
    if st.session_state.get("rol_handheld") != "admin":
        st.warning("⛔ Solo los administradores pueden generar LPNs.")
        return

    with st.form("form_lpn"):
        tipo_etiqueta = st.selectbox("Tipo de etiqueta", ["Etiquetas IB", "Etiquetas OB"])
        cantidad = st.number_input("Cantidad a generar", min_value=1, step=1)
        submitted = st.form_submit_button("Generar")

        if submitted:
            usuario = st.session_state.get("codigo_empleado")
            bodega = st.session_state.get("bodega", "61")
            if not usuario or not bodega:
                st.error("Usuario o bodega no definidos en sesión.")
                return

            try:
                libro = st.session_state.get("libro_lpn")
                if not libro:
                    from google_sheets import conectar_sit_hh
                    libro = conectar_sit_hh()
                    st.session_state.libro_lpn = libro

                nuevos = generate_lpns(cantidad, usuario, bodega, tipo_etiqueta, libro)
                st.success(f"{len(nuevos)} LPNs generados exitosamente.")
                st.dataframe(pd.DataFrame(nuevos, columns=["Número LPN", "Fecha creación", "Creado por", "Estado", "Bodega"]))
            except Exception as e:
                st.error(f"Error al generar LPNs: {e}")
