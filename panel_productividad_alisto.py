import streamlit as st
import pandas as pd
from datetime import datetime
import pytz

cr_timezone = pytz.timezone("America/Costa_Rica")

def mostrar_panel_alisto(conectar_funcion):
    st.title("📊 Panel de Productividad - Alisto")

    # Conectar a la hoja 'Productividad'
    try:
        hoja = conectar_funcion().worksheet("Productividad")
    except Exception:
        st.error("❌ No se pudo acceder a la hoja 'Productividad'. Verifica que exista en Google Sheets.")
        st.stop()

    datos = hoja.get_all_values()
    if not datos or len(datos[0]) == 0:
        st.warning("⚠️ No se encontraron datos en la hoja 'Productividad'.")
        return

    # Crear DataFrame y normalizar columnas
    df = pd.DataFrame(datos[1:], columns=datos[0])
    df.columns = df.columns.str.strip().str.lower()

    # Renombrar columnas esperadas
    df = df.rename(columns={
        "fecha": "fecha",
        "nombre del empleado": "empleado",
        "placa": "placa",
        "hora de inicio": "inicio",
        "hora de fin": "fin",
        "cantidad líneas - unidades": "cantidad"
    })

    # Validar que existan las columnas necesarias
    columnas_requeridas = ["fecha", "inicio", "fin", "empleado", "placa", "cantidad"]
    faltantes = [col for col in columnas_requeridas if col not in df.columns]
    if faltantes:
        st.error(f"🚫 Faltan columnas en la hoja: {', '.join(faltantes)}")
        return

    # Conversión de tipos
    df["fecha"] = pd.to_datetime(df["fecha"], errors="coerce")
    df["inicio"] = pd.to_datetime(df["inicio"], errors="coerce")
    df["fin"] = pd.to_datetime(df["fin"], errors="coerce")
    df["cantidad"] = pd.to_numeric(df["cantidad"], errors="coerce")
    df["duracion"] = (df["fin"] - df["inicio"]).dt.total_seconds() / 3600

    # Filtros con claves únicas
    empleados = sorted(df["empleado"].dropna().unique())
    fecha_ini = st.date_input(
        "Desde",
        value=datetime.now(cr_timezone).date(),
        key="filtro_fecha_ini_alisto"
    )
    fecha_fin = st.date_input(
        "Hasta",
        value=datetime.now(cr_timezone).date(),
        key="filtro_fecha_fin_alisto"
    )
    empleado_sel = st.selectbox(
        "Filtrar por empleado",
        ["Todos"] + empleados,
        key="filtro_empleado_alisto"
    )

    df_filtrado = df[
        (df["fecha"].dt.date >= fecha_ini) &
        (df["fecha"].dt.date <= fecha_fin)
    ]
    if empleado_sel != "Todos":
        df_filtrado = df_filtrado[df_filtrado["empleado"] == empleado_sel]

    # Mostrar registros
    st.subheader("🗂️ Registros de Alisto")
    st.dataframe(df_filtrado, use_container_width=True)

    # Totales por placa
    st.subheader("🔢 Unidades Alistadas por Placa")
    resumen_placa = df_filtrado.groupby("placa")["cantidad"].sum().reset_index(name="Total Unidades")
    st.dataframe(resumen_placa, use_container_width=True)

    # Ranking por horas
    st.subheader("⏱️ Ranking por Horas de Alisto")
    ranking = df_filtrado.groupby("empleado")["duracion"].sum().reset_index(name="Horas Totales")
    ranking = ranking.sort_values(by="Horas Totales", ascending=False)
    st.dataframe(ranking, use_container_width=True)
    st.bar_chart(ranking.set_index("empleado"), use_container_width=True)

    # Eficiencia por empleado
    st.subheader("💡 Unidades Alistadas por Hora")
    eficiencia = df_filtrado.groupby("empleado").apply(
        lambda x: x["cantidad"].sum() / x["duracion"].sum() if x["duracion"].sum() > 0 else 0
    ).reset_index(name="Unidades/Hora")
    st.dataframe(eficiencia, use_container_width=True)

    # Exportación CSV
    csv = df_filtrado.to_csv(index=False).encode("utf-8")
    st.download_button(
        "📥 Descargar CSV",
        csv,
        "productividad_alisto.csv",
        "text/csv",
        key="descarga_csv_alisto"
    )
