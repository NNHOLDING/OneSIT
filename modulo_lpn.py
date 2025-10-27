import streamlit as st
import pandas as pd
from datetime import datetime

def generate_lpns(cantidad, usuario, bodega, tipo_etiqueta):
    pais_codigo = "506"
    fecha_actual = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    estado = "activo"
    lpns = []

    # Determinar prefijo
    prefijo = "IB" if tipo_etiqueta == "Etiquetas IB" else "OB"
    base = f"{prefijo}{bodega}{pais_codigo}"

    # Obtener consecutivo inicial (puedes reemplazar esto con lectura desde hoja si lo deseas)
    consecutivo_inicial = 1  # Aquí podrías consultar la hoja para obtener el último consecutivo

    for i in range(cantidad):
        consecutivo = str(consecutivo_inicial + i).zfill(5)
        numero_lpn = f"{base}{consecutivo}"
        lpns.append([numero_lpn, fecha_actual, usuario, estado, bodega])

    return lpns

def mostrar_formulario_lpn():
    if st.session_state.get("rol_handheld") == "admin":
        st.subheader("🧾 Generar LPNs")
        with st.form("form_lpn"):
            tipo_etiqueta = st.selectbox("Tipo de etiqueta", ["Etiquetas IB", "Etiquetas OB"])
            cantidad = st.number_input("Cantidad a generar", min_value=1, step=1)
            submitted = st.form_submit_button("Generar")
            if submitted:
                if cantidad > 0:
                    usuario = st.session_state.get("codigo_empleado")
                    bodega = st.session_state.get("bodega", "61")  # Puedes ajustar cómo se define la bodega
                    if usuario and bodega:
                        nuevos = generate_lpns(cantidad, usuario, bodega, tipo_etiqueta)
                        st.success(f"{len(nuevos)} LPNs generados exitosamente.")
                        st.dataframe(pd.DataFrame(nuevos, columns=["Número LPN", "Fecha creación", "Creado por", "Estado", "Bodega"]))
                        # Aquí podrías agregar lógica para guardar en Google Sheets
                    else:
                        st.error("Usuario o bodega no definidos en sesión.")
                else:
                    st.warning("La cantidad debe ser mayor a cero.")
    else:
        st.info("Solo los usuarios con rol Admin pueden generar LPNs.")