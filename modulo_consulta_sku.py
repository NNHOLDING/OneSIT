import streamlit as st
import pandas as pd

def cargar_hoja(libro, nombre_hoja):
    try:
        hoja = libro.worksheet(nombre_hoja)
        datos = hoja.get_all_values()
        if not datos or len(datos) < 2:
            return pd.DataFrame()
        encabezados = [col.strip() for col in datos[0]]
        return pd.DataFrame(datos[1:], columns=encabezados)
    except Exception as e:
        st.error(f"❌ Error al cargar la hoja '{nombre_hoja}': {e}")
        return pd.DataFrame()

def construir_ubicacion(row):
    pasillo = str(row['Pasillo']).strip().upper()
    if not pasillo.startswith("P"):
        pasillo = f"P{pasillo.zfill(2)}"
    tramo = str(row['Tramo']).strip()
    nivel = str(row['Nivel']).strip()
    posicion = str(row['Posición']).strip()
    return f"Pasillo {pasillo} - Tramo {tramo} - Nivel {nivel} - Posición {posicion}"

def mostrar_consulta_sku(conectar_sit_hh):
    st.title("🔍 Consulta de SKU por código SAP")

    codigo_sap = st.text_input("Ingrese el código SAP del producto").strip()

    if codigo_sap and not codigo_sap.isdigit():
        st.error("🚫 El código SAP debe contener solo números.")
        return

    buscar = st.button("🔎 Buscar")

    if buscar and codigo_sap:
        try:
            libro = conectar_sit_hh()
        except Exception as e:
            st.error(f"❌ Error al conectar con Google Sheets: {e}")
            return

        df_recibo = cargar_hoja(libro, "TRecibo")
        if df_recibo.empty:
            st.warning("⚠️ No se pudo cargar la hoja TRecibo.")
            return

        df_sku = df_recibo[df_recibo["sap"].str.strip() == codigo_sap]

        if df_sku.empty:
            st.warning("⚠️ No se encontraron registros para ese código SAP.")
            return

        df_ubicaciones = cargar_hoja(libro, "Ubicaciones")
        if df_ubicaciones.empty:
            st.warning("⚠️ No se pudo cargar la hoja Ubicaciones.")
            return

        df_ubicadas = df_ubicaciones[df_ubicaciones["Estado"].str.strip().str.lower() == "ocupado"]

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
