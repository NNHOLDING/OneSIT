import streamlit as st
import pandas as pd

def mostrar_opcion_exportar(libro):
    st.subheader("📤 Exportar hoja de ubicaciones")

    try:
        hoja = libro.worksheet("Ubicaciones")
        datos = hoja.get_all_values()
        encabezados = [col.strip() for col in datos[0]]
        df = pd.DataFrame(datos[1:], columns=encabezados)
    except Exception as e:
        st.error(f"No se pudo cargar la hoja Ubicaciones: {e}")
        return

    if df.empty:
        st.warning("La hoja Ubicaciones está vacía.")
        return

    archivo_csv = df.to_csv(index=False).encode("utf-8")
    st.download_button(
        label="⬇️ Descargar CSV",
        data=archivo_csv,
        file_name="Ubicaciones.csv",
        mime="text/csv"
    )