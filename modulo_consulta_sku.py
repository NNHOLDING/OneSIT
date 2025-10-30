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

    codigos_sap_input = st.text_input("Ingrese uno o varios códigos SAP separados por coma").strip()
    buscar = st.button("🔎 Buscar")

    if buscar and codigos_sap_input:
        codigos_sap = [c.strip() for c in codigos_sap_input.split(",") if c.strip().isdigit()]
        if not codigos_sap:
            st.error("🚫 Debes ingresar al menos un código SAP válido (solo números).")
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

        st.subheader("📋 Ubicaciones del producto")
        selected_row = st.data_editor(
            df_resultado[[
                "sap", "LPN", "Ubicación", "Cantidad", "Fecha caducidad", "Fecha registro", "⚠️ Vencimiento"
            ]],
            use_container_width=True,
            hide_index=True,
            num_rows="dynamic",
            column_order=["sap", "LPN", "Ubicación", "Cantidad", "Fecha caducidad", "Fecha registro", "⚠️ Vencimiento"],
            key="sku_editor",
            disabled=["sap", "LPN", "Ubicación", "Fecha registro", "⚠️ Vencimiento"],
        )

        if "sku_editor" in st.session_state:
            selected_index = st.session_state["sku_editor"]["edited_rows"]
            if selected_index:
                idx = list(selected_index.keys())[0]
                fila = df_resultado.iloc[idx]

                if st.button("✏️ Editar fila seleccionada"):
                    with st.modal("🛠️ Editar ubicación"):
                        st.text_input("Código SAP", value=fila["sap"], disabled=True)
                        st.text_input("LPN", value=fila["LPN"], disabled=True)
                        st.text_input("Ubicación", value=fila["Ubicación"], disabled=True)
                        cantidad_editada = st.number_input("Cantidad", value=int(fila["Cantidad"]), min_value=0)
                        fecha_editada = st.date_input("Fecha de caducidad", value=fila["Fecha caducidad"].date() if pd.notnull(fila["Fecha caducidad"]) else datetime.today())
                        if st.form_submit_button("💾 Guardar cambios"):
                            hoja = libro.worksheet("TRecibo")
                            lpn = fila["LPN"]
                            fila_original = df_recibo[df_recibo["LPN"] == lpn].index
                            if not fila_original.empty:
                                idx_real = fila_original[0] + 2
                                hoja.update_cell(idx_real, df_recibo.columns.get_loc("Cantidad") + 1, str(cantidad_editada))
                                hoja.update_cell(idx_real, df_recibo.columns.get_loc("Fecha caducidad") + 1, fecha_editada.strftime("%Y-%m-%d"))
                                st.success("✅ Cambios guardados correctamente.")
                            else:
                                st.error("❌ No se pudo encontrar la fila original para actualizar.")
