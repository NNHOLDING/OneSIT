import streamlit as st
import pandas as pd
from datetime import datetime
import pytz

cr_timezone = pytz.timezone("America/Costa_Rica")

def mostrar_panel_alisto(conectar_funcion):
    st.title("📊 Panel de Productividad - Alisto")

    # Conectar a la hoja
    try:
        hoja = conectar_funcion().worksheet("Productividad")
    except Exception:
        st.error("❌ No se pudo acceder a la hoja 'Productividad'.")
        st.stop()

    datos = hoja.get_all_values()
    if not datos or len(datos[0]) == 0:
        st.warning("⚠️ No hay datos en la hoja.")
        return

    df = pd.DataFrame(datos[1:], columns=datos[0])
    df.columns = df.columns.str.strip().str.lower()
    df = df.rename(columns={
        "fecha": "fecha",
        "nombre del empleado": "empleado",
        "placa": "placa",
        "hora de inicio": "inicio",
        "hora de fin": "fin",
        "cantidad líneas - unidades": "cantidad"
    })

    requeridas = ["fecha", "inicio", "fin", "empleado", "placa", "cantidad"]
    faltantes = [col for col in requeridas if col not in df.columns]
    if faltantes:
        st.error(f"🚫 Faltan columnas: {', '.join(faltantes)}")
        return

    # Procesamiento
    df["fecha"] = pd.to_datetime(df["fecha"], errors="coerce")
    df["inicio"] = pd.to_datetime(df["inicio"], errors="coerce")
    df["fin"] = pd.to_datetime(df["fin"], errors="coerce")
    df["cantidad"] = pd.to_numeric(df["cantidad"], errors="coerce")
    df["duracion"] = (df["fin"] - df["inicio"]).dt.total_seconds() / 3600

    # Filtros
    empleados = sorted(df["empleado"].dropna().unique())
    fecha_ini = st.date_input("Desde", value=datetime.now(cr_timezone).date(), key="filtro_fecha_ini")
    fecha_fin = st.date_input("Hasta", value=datetime.now(cr_timezone).date(), key="filtro_fecha_fin")
    empleado_sel = st.selectbox("Empleado", ["Todos"] + empleados, key="filtro_empleado")

    df_filtrado = df[
        (df["fecha"].dt.date >= fecha_ini) &
        (df["fecha"].dt.date <= fecha_fin)
    ]
    if empleado_sel != "Todos":
        df_filtrado = df_filtrado[df_filtrado["empleado"] == empleado_sel]

    # Registros
    st.subheader("📋 Registros filtrados")
    st.dataframe(df_filtrado, use_container_width=True)

    # Unidades por placa
    st.subheader("🚛 Unidades por Placa")
    resumen_placa = df_filtrado.groupby("placa")["cantidad"].sum().reset_index(name="Total Unidades")
    st.dataframe(resumen_placa, use_container_width=True)
    st.bar_chart(resumen_placa.set_index("placa"), use_container_width=True)

    # Ranking por duración
    st.subheader("⏱️ Ranking por Horas")
    ranking = df_filtrado.groupby("empleado")["duracion"].sum().reset_index(name="Horas Totales")
    ranking = ranking.sort_values(by="Horas Totales", ascending=False)
    st.dataframe(ranking, use_container_width=True)
    st.bar_chart(ranking.set_index("empleado"), use_container_width=True)

    # Eficiencia por empleado
    st.subheader("💡 Unidades/Hora por Empleado")
    eficiencia = df_filtrado.groupby("empleado").agg({
        "cantidad": "sum",
        "duracion": "sum"
    })
    eficiencia["Unidades/Hora"] = eficiencia["cantidad"] / eficiencia["duracion"]
    eficiencia = eficiencia.reset_index()[["empleado", "Unidades/Hora"]]
    eficiencia = eficiencia.dropna()
    st.dataframe(eficiencia, use_container_width=True)

    # Eficiencia histórica semanal
    st.subheader("📆 Eficiencia Histórica (Semanal)")
    df_filtrado["semana"] = df_filtrado["fecha"].dt.to_period("W").astype(str)
    eficiencia_semana = df_filtrado.groupby("semana").agg({
        "cantidad": "sum",
        "duracion": "sum"
    })
    eficiencia_semana["Unidades/Hora"] = eficiencia_semana["cantidad"] / eficiencia_semana["duracion"]
    eficiencia_semana = eficiencia_semana.reset_index()[["semana", "Unidades/Hora"]]
    eficiencia_semana = eficiencia_semana.dropna()
    st.dataframe(eficiencia_semana, use_container_width=True)
    st.line_chart(eficiencia_semana.set_index("semana"), use_container_width=True)

    # Exportación
    csv = df_filtrado.to_csv(index=False).encode("utf-8")
    st.download_button("📥 Descargar CSV", csv, "productividad_alisto.csv", "text/csv", key="descarga_csv")

    resumen_semanal = df_filtrado.groupby("semana").agg({
        "cantidad": "sum",
        "duracion": "sum"
    }).reset_index()
    csv_semanal = resumen_semanal.to_csv(index=False).encode("utf-8")
    st.download_button("📥 Descargar resumen semanal", csv_semanal, "resumen_semanal.csv", "text/csv", key="csv_semanal")
