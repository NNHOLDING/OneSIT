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
    st.title("🔍 Consulta avanzada de SKU")

    codigos_sap_input = st.text_input("Ingrese uno o varios códigos SAP separados por coma").strip()
    cantidad_minima = st.number_input("Cantidad mínima", min_value=0, value=0)
    fecha_caducidad_min = st.date_input("Fecha de caducidad mínima", value=datetime.today())

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

        # Formatear columnas
        df_resultado["Cantidad"] = pd.to_numeric(df_resultado["Cantidad"], errors="coerce").fillna(0)
        df_resultado["Fecha caducidad"] = pd.to_datetime(df_resultado["Fecha caducidad"], errors="coerce")
        df_resultado["Ubicación"] = df_resultado.apply(construir_ubicacion, axis=1)

        # Aplicar filtros
        df_filtrado = df_resultado[
            (df_resultado["Cantidad"] >= cantidad_minima) &
            (df_resultado["Fecha caducidad"] >= pd.to_datetime(fecha_caducidad_min))
        ]

        if df_filtrado.empty:
            st.warning("⚠️ No hay resultados que cumplan con los filtros aplicados.")
            return

        # Alertas de vencimiento
        hoy = datetime.today()
        df_filtrado["⚠️ Vencimiento"] = df_filtrado["Fecha caducidad"].apply(
            lambda x: "Próximo" if pd.notnull(x) and x <= hoy + timedelta(days=30) else ""
        )

        st.subheader("📋 Ubicaciones del producto")
        seleccion = st.radio("Selecciona una fila para editar", df_filtrado.index.tolist(), horizontal=True)

        st.dataframe(df_filtrado[[
            "sap", "LPN", "Ubicación", "Cantidad", "Fecha caducidad", "Fecha registro", "⚠️ Vencimiento"
        ]].sort_values(by="Ubicación"))

        # Formulario de edición contextual
        st.markdown("### ✏️ Editar cantidad y fecha de caducidad")
        fila = df_filtrado.loc[seleccion]
        nueva_cantidad = st.number_input("Nueva cantidad", value=int(fila["Cantidad"]), min_value=0)
        nueva_fecha = st.date_input("Nueva fecha de caducidad", value=fila["Fecha caducidad"].date() if pd.notnull(fila["Fecha caducidad"]) else datetime.today())

        if st.button("💾 Guardar cambios"):
            hoja = libro.worksheet("TRecibo")
            lpn = fila["LPN"]
            fila_original = df_recibo[df_recibo["LPN"] == lpn].index
            if not fila_original.empty:
                idx = fila_original[0] + 2  # +2 por encabezado y base 1
                hoja.update_cell(idx, df_recibo.columns.get_loc("Cantidad") + 1, str(nueva_cantidad))
                hoja.update_cell(idx, df_recibo.columns.get_loc("Fecha caducidad") + 1, nueva_fecha.strftime("%Y-%m-%d"))
                st.success("✅ Cambios guardados correctamente.")
            else:
                st.error("❌ No se pudo encontrar la fila original para actualizar.")
