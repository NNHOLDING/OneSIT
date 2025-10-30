import streamlit as st
import pandas as pd

def cargar_hoja(libro, nombre_hoja):
    try:
        hoja = libro.worksheet(nombre_hoja)
        datos = hoja.get_all_values()
        return pd.DataFrame(datos[1:], columns=datos[0])
    except Exception as e:
        st.error(f"❌ Error al cargar la hoja '{nombre_hoja}': {e}")
        return pd.DataFrame()

def construir_ubicacion(row):
    return f"Pasillo {row['Pasillo']} - Tramo {row['Tramo']} - Nivel {row['Nivel']} - Posición {row['Posición']}"

def mostrar_consulta_sku(conectar_sit_hh):
    st.title("🔍 Consulta de SKU por código SAP")

    codigo_sap = st.text_input("Ingrese el código SAP del producto")

    if codigo_sap and not codigo_sap.isdigit():
        st.error("🚫 El código SAP debe contener solo números.")
        return

    buscar = st.button("🔎 Buscar")

    if buscar and codigo_sap:
        libro = conectar_sit_hh()

        df_recibo = cargar_hoja(libro, "TRecibo")
        if df_recibo.empty:
            return

        df_sku = df_recibo[df_recibo["sap"] == codigo_sap]

        if df_sku.empty:
            st.warning("⚠️ No se encontraron registros para ese código SAP.")
            return

        df_ubicaciones = cargar_hoja(libro, "Ubicaciones")
        if df_ubicaciones.empty:
            return

        df_ubicadas = df_ubicaciones[df_ubicaciones["Estado"] == "Ocupado"]

        df_resultado = pd.merge(
            df_sku,
            df_ubicadas,
            left_on="LPN",
            right_on="LPN Asignado",
            how="inner"
        )

        if df_resultado.empty:
            st.info("ℹ️ No hay ubicaciones ocupadas para este SKU.")
            return

        df_resultado["Ubicación"] = df_resultado.apply(construir_ubicacion, axis=1)

        resultado_final = df_resultado[[
            "LPN", "Ubicación", "Cantidad", "Fecha caducidad", "Fecha registro"
        ]].sort_values(by="Ubicación")

        st.subheader("📋 Ubicaciones del producto")
        st.dataframe(resultado_final)

        # Botón de descarga
        csv = resultado_final.to_csv(index=False).encode("utf-8")
        st.download_button(
            label="⬇️ Descargar resultados en CSV",
            data=csv,
            file_name=f"ubicaciones_sap_{codigo_sap}.csv",
            mime="text/csv"
        )
