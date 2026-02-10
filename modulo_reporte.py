import streamlit as st
import pandas as pd

def mostrar_reporte(conectar_sit_hh):
    # Conexión a Google Sheets
    libro = conectar_sit_hh()
    hoja = libro.worksheet("TRecibo")
    datos = hoja.get_all_values()

    # Convertir a DataFrame
    df = pd.DataFrame(datos[1:], columns=datos[0])

    # Selector de LPN
    lpn_unicos = df["LPN"].unique().tolist()
    lpn_seleccionado = st.selectbox("Selecciona el LPN", lpn_unicos)

    # Filtrar por LPN
    df_filtrado = df[df["LPN"] == lpn_seleccionado]

    # Mostrar rejilla
    st.dataframe(df_filtrado, use_container_width=True)

    # Botón para descargar en Excel
    if st.button("📥 Descargar en Excel"):
        # Convertir a Excel en memoria
        excel_buffer = pd.ExcelWriter("reporte.xlsx", engine="xlsxwriter")
        df_filtrado.to_excel(excel_buffer, index=False, sheet_name="Reporte")
        excel_buffer.close()

        # Descargar
        with open("reporte.xlsx", "rb") as f:
            st.download_button(
                label="Descargar archivo",
                data=f,
                file_name=f"Reporte_{lpn_seleccionado}.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            )