import streamlit as st
import pandas as pd
from datetime import datetime, timedelta

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
    tramo = str(row['Tramo']).strip().zfill(2)
    nivel = str(row['Nivel']).strip().zfill(2)
    posicion = str(row['Posición']).strip().zfill(2)
    return f"{pasillo}-{tramo}-{nivel}-{posicion}"

def mostrar_consulta_sku(conectar_sit_hh):
    st.title("🔍 Consulta de SKU por código SAP")

    # Inicializar estado
    if "datos_sku" not in st.session_state:
        st.session_state["datos_sku"] = None
    if "df_recibo" not in st.session_state:
        st.session_state["df_recibo"] = None
    if "libro" not in st.session_state:
        st.session_state["libro"] = None

    codigos_sap_input = st.text_input("Ingrese uno o varios códigos SAP separados por coma").strip()

    if st.button("🔎 Buscar"):
        codigos_sap = [c.strip() for c in codigos_sap_input.split(",") if c.strip().isdigit()]
        if not codigos_sap:
            st.error("🚫 Debes ingresar al menos un código SAP válido.")
            return

        try:
            libro = conectar_sit_hh()
        except Exception as e:
            st.error(f"❌ Error al conectar con Google Sheets: {e}")
            return

        df_recibo = cargar_hoja(libro, "TRecibo")
        df_ubicaciones = cargar_hoja(libro, "Ubicaciones")

        if df_recibo.empty or df_ubicaciones.empty:
            st.warning("⚠️ Las hojas necesarias están vacías o mal formateadas.")
            return

        df_recibo["sap"] = df_recibo["sap"].str.strip()
        df_sku = df_recibo[df_recibo["sap"].isin(codigos_sap)]

        if df_sku.empty:
            st.warning("⚠️ No se encontraron registros para los códigos SAP ingresados.")
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
            st.info("ℹ️ No hay ubicaciones ocupadas para estos SKUs.")
            return

        df_resultado["Cantidad"] = pd.to_numeric(df_resultado["Cantidad"], errors="coerce").fillna(0)
        df_resultado["Fecha caducidad"] = pd.to_datetime(df_resultado["Fecha caducidad"], errors="coerce")
        df_resultado["Ubicación"] = df_resultado.apply(construir_ubicacion, axis=1)

        hoy = datetime.today()
        df_resultado["⚠️ Vencimiento"] = df_resultado["Fecha caducidad"].apply(
            lambda x: "Próximo" if pd.notnull(x) and x <= hoy + timedelta(days=30) else ""
        )

        df_resultado = df_resultado.reset_index(drop=True)

        # Guardar en sesión
        st.session_state["datos_sku"] = df_resultado
        st.session_state["df_recibo"] = df_recibo
        st.session_state["libro"] = libro

    # Mostrar tabla si hay datos
    if st.session_state["datos_sku"] is not None:
        df_resultado = st.session_state["datos_sku"]
        st.subheader("📋 Ubicaciones del producto")
        edited_df = st.data_editor(
            df_resultado[[
                "sap", "LPN", "Ubicación", "Cantidad", "Fecha caducidad", "Fecha registro", "⚠️ Vencimiento"
            ]],
            use_container_width=True,
            hide_index=True,
            disabled=["sap", "LPN", "Ubicación", "Fecha registro", "⚠️ Vencimiento"],
            key="sku_editor"
        )

        if st.button("💾 Guardar cambios"):
            actualizados = 0
            for i, fila_editada in edited_df.iterrows():
                original = df_resultado.iloc[i]
                if (
                    str(fila_editada["Cantidad"]) != str(original["Cantidad"])
                    or str(fila_editada["Fecha caducidad"])[:10] != str(original["Fecha caducidad"])[:10]
                ):
                    hoja = st.session_state["libro"].worksheet("TRecibo")
                    lpn = original["LPN"]
                    fila_original = st.session_state["df_recibo"][st.session_state["df_recibo"]["LPN"] == lpn].index
                    if not fila_original.empty:
                        idx_real = fila_original[0] + 2
                        hoja.update_cell(idx_real, st.session_state["df_recibo"].columns.get_loc("Cantidad") + 1, str(fila_editada["Cantidad"]))
                        hoja.update_cell(idx_real, st.session_state["df_recibo"].columns.get_loc("Fecha caducidad") + 1, pd.to_datetime(fila_editada["Fecha caducidad"]).strftime("%Y-%m-%d"))
                        actualizados += 1
            if actualizados > 0:
                st.success(f"✅ {actualizados} registro(s) actualizado(s) correctamente.")
            else:
                st.info("ℹ️ No se detectaron cambios para guardar.")
