import streamlit as st
import pandas as pd

def mostrar_consulta_sku(conectar_sit_hh):
    st.title("🔍 Consulta de SKU por código SAP")

    codigo_sap = st.text_input("Ingrese el código SAP del producto")

    if codigo_sap:
        libro = conectar_sit_hh()

        # Hoja TRecibo
        hoja_recibo = libro.worksheet("TRecibo")
        datos_recibo = hoja_recibo.get_all_values()
        df_recibo = pd.DataFrame(datos_recibo[1:], columns=datos_recibo[0])

        # Filtrar por SAP
        df_sku = df_recibo[df_recibo["sap"] == codigo_sap]

        if df_sku.empty:
            st.warning("⚠️ No se encontraron registros para ese código SAP.")
            return

        # Hoja Ubicaciones
        hoja_ubicaciones = libro.worksheet("Ubicaciones")
        datos_ubicaciones = hoja_ubicaciones.get_all_values()
        df_ubicaciones = pd.DataFrame(datos_ubicaciones[1:], columns=datos_ubicaciones[0])

        # Filtrar ubicaciones con LPNs del SKU
        df_resultado = pd.merge(
            df_sku,
            df_ubicaciones[df_ubicaciones["Estado"] == "Ocupado"],
            left_on="LPN",
            right_on="LPN Asignado",
            how="inner"
        )

        # Crear columna ubicación
        df_resultado["Ubicación"] = (
            "Pasillo " + df_resultado["Pasillo"] + " - Tramo " + df_resultado["Tramo"] +
            " - Nivel " + df_resultado["Nivel"] + " - Posición " + df_resultado["Posición"]
        )

        # Mostrar grilla
        st.subheader("📋 Ubicaciones del producto")
        st.dataframe(df_resultado[[
            "LPN", "Ubicación", "Cantidad", "Fecha caducidad", "Fecha registro"
        ]].sort_values(by="Ubicación"))