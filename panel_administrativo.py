import streamlit as st
import pandas as pd
from datetime import datetime

def mostrar_panel_administrativo(conectar_sit_hh, cr_timezone):
    st.title("📋 Panel Administrativo")
    hoja = conectar_sit_hh().worksheet("HH")
    datos = hoja.get_all_values()

    if datos and len(datos[0]) > 0:
        df = pd.DataFrame(datos[1:], columns=datos[0])
        df.columns = df.columns.str.strip().str.lower()
        df["fecha"] = pd.to_datetime(df["fecha"], errors="coerce")

        usuarios = sorted(df["nombre"].dropna().unique())
        fecha_ini = st.date_input("Desde", value=datetime.now(cr_timezone).date())
        fecha_fin = st.date_input("Hasta", value=datetime.now(cr_timezone).date())
        usuario_sel = st.selectbox("Filtrar por Usuario", ["Todos"] + usuarios)

        df_filtrado = df[
            (df["fecha"].dt.date >= fecha_ini) &
            (df["fecha"].dt.date <= fecha_fin)
        ]
        if usuario_sel != "Todos":
            df_filtrado = df_filtrado[df_filtrado["nombre"] == usuario_sel]

        st.subheader("📑 Registros")
        st.dataframe(df_filtrado)

        hoy = datetime.now(cr_timezone).date()
        if "estatus" in df.columns:
            entregados_hoy = df[
                (df["fecha"].dt.date == hoy) & (df["estatus"].str.lower() == "entregado")
            ]
            devueltos_hoy = df[
                (df["fecha"].dt.date == hoy) & (df["estatus"].str.lower() == "devuelto")
            ]

            st.subheader("✅ Registros Entregados Hoy")
            st.dataframe(entregados_hoy)

            st.subheader("📤 Registros Devueltos Hoy")
            st.dataframe(devueltos_hoy)

            st.markdown("### 📊 Resumen de Movimientos Hoy")
            col1, col2 = st.columns(2)
            with col1:
                st.metric("Entregados", len(entregados_hoy))
            with col2:
                st.metric("Devueltos", len(devueltos_hoy))
        else:
            st.info("ℹ️ No se encontró la columna 'estatus' para mostrar entregas y devoluciones de hoy.")

        csv = df_filtrado.to_csv(index=False).encode("utf-8")
        st.download_button("📥 Descargar CSV", csv, "handhelds.csv", "text/csv")

        st.subheader("📊 Actividad por Usuario")
        resumen = df_filtrado.groupby("nombre").size().reset_index(name="Registros")
        st.dataframe(resumen)
        st.bar_chart(resumen.set_index("nombre"))

        st.subheader("🔧 Actividad por Equipo")
        resumen_eq = df_filtrado.groupby("equipo").size().reset_index(name="Movimientos")
        st.dataframe(resumen_eq)
        st.bar_chart(resumen_eq.set_index("equipo"))
    else:
        st.warning("⚠️ No se encontró la columna 'nombre' en los datos.")