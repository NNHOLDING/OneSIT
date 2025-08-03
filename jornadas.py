import streamlit as st
import pandas as pd
from datetime import datetime
import pytz

# ✅ Zona horaria Costa Rica
cr_timezone = pytz.timezone("America/Costa_Rica")

# 📋 Función principal del módulo
def mostrar_jornadas(conectar_funcion):
    st.title("🕒 Registro de Jornadas")

    try:
        hoja = conectar_funcion().worksheet("Jornadas")
        datos = hoja.get_all_values()
        df = pd.DataFrame(datos[1:], columns=datos[0])

        # 🗃️ Convertir fechas y horas
        df["fecha"] = pd.to_datetime(df["fecha"], errors="coerce")
        df["fecha cierre"] = pd.to_datetime(df["fecha cierre"], errors="coerce")
        df["Total horas extras"] = pd.to_numeric(df["Total horas extras"], errors="coerce")

        # 🎚️ Filtros
        fecha_ini = st.date_input("📅 Desde", value=datetime.now(cr_timezone).date())
        fecha_fin = st.date_input("📅 Hasta", value=datetime.now(cr_timezone).date())

        usuarios = sorted(df["usuario"].dropna().unique())
        usuario_sel = st.selectbox("👤 Filtrar por Usuario", ["Todos"] + usuarios)

        bodegas = sorted(df["Bodega"].dropna().unique())
        bodega_sel = st.selectbox("🏬 Filtrar por Bodega", ["Todas"] + bodegas)

        # 📐 Filtrado dinámico
        df_filtrado = df[
            (df["fecha"].dt.date >= fecha_ini) &
            (df["fecha"].dt.date <= fecha_fin)
        ]
        if usuario_sel != "Todos":
            df_filtrado = df_filtrado[df_filtrado["usuario"] == usuario_sel]
        if bodega_sel != "Todas":
            df_filtrado = df_filtrado[df_filtrado["Bodega"] == bodega_sel]

        # 🧮 Mostrar tabla filtrada
        st.subheader("📑 Registros filtrados")
        st.dataframe(df_filtrado)

        # 💾 Botón de descarga
        csv = df_filtrado.to_csv(index=False).encode("utf-8")
        st.download_button("📥 Descargar CSV", csv, "jornadas.csv", "text/csv")

        # 📊 Resumen por usuario
        st.subheader("📈 Total de Jornadas por Usuario")
        jornadas = df_filtrado.groupby("usuario").size().reset_index(name="Jornadas")
        st.dataframe(jornadas)
        st.bar_chart(jornadas.set_index("usuario"))

        # 📊 Resumen de horas extras por bodega
        st.subheader("⏱️ Horas Extras por Bodega")
        extras = df_filtrado.groupby("Bodega")["Total horas extras"].sum().reset_index()
        st.dataframe(extras)
        st.bar_chart(extras.set_index("Bodega"))

    except Exception as e:
        st.error(f"❌ Error al cargar la hoja de Jornadas: {e}")