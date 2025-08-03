import streamlit as st
import pandas as pd
from datetime import datetime
import pytz

cr_timezone = pytz.timezone("America/Costa_Rica")

def mostrar_panel_alisto(conectar_funcion):
    st.title("📊 Panel de Productividad - Alisto")

    hoja = conectar_funcion().worksheet("ALISTO")
    datos = hoja.get_all_values()
    if not datos or len(datos[0]) == 0:
        st.warning("⚠️ No se encontraron datos en la hoja 'ALISTO'.")
        return

    df = pd.DataFrame(datos[1:], columns=datos[0])
    df.columns = df.columns.str.lower()
    df["fecha"] = pd.to_datetime(df["fecha"], errors="coerce")
    df["inicio"] = pd.to_datetime(df["inicio"], errors="coerce")
    df["fin"] = pd.to_datetime(df["fin"], errors="coerce")
    df["cantidad"] = pd.to_numeric(df["cantidad"], errors="coerce")
    df["duracion"] = (df["fin"] - df["inicio"]).dt.total_seconds() / 3600

    empleados = sorted(df["empleado"].dropna().unique())
    fecha_ini = st.date_input("Desde", value=datetime.now(cr_timezone).date())
    fecha_fin = st.date_input("Hasta", value=datetime.now(cr_timezone).date())
    empleado_sel = st.selectbox("Filtrar por empleado", ["Todos"] + empleados)

    df_filtrado = df[
        (df["fecha"].dt.date >= fecha_ini) &
        (df["fecha"].dt.date <= fecha_fin)
    ]
    if empleado_sel != "Todos":
        df_filtrado = df_filtrado[df_filtrado["empleado"] == empleado_sel]

    st.subheader("🗂️ Registros de Alisto")
    st.dataframe(df_filtrado)

    st.subheader("🔢 Totales por Placa")
    resumen_placa = df_filtrado.groupby("placa")["cantidad"].sum().reset_index(name="Total Alistado")
    st.dataframe(resumen_placa)

    st.subheader("⏱️ Ranking por Duración Total")
    ranking = df_filtrado.groupby("empleado")["duracion"].sum().reset_index(name="Horas")
    ranking = ranking.sort_values(by="Horas", ascending=False)
    st.dataframe(ranking)
    st.bar_chart(ranking.set_index("empleado"))

    st.subheader("💡 Promedio de Alisto por Hora")
    eficiencia = df_filtrado.groupby("empleado").apply(
        lambda x: x["cantidad"].sum() / x["duracion"].sum() if x["duracion"].sum() > 0 else 0
    ).reset_index(name="Unidades por Hora")
    st.dataframe(eficiencia)

    csv = df_filtrado.to_csv(index=False).encode("utf-8")
    st.download_button("📥 Descargar CSV", csv, "alisto_productividad.csv", "text/csv")