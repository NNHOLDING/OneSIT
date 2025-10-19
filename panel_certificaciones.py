import streamlit as st
import pandas as pd
from datetime import datetime

def mostrar_panel_certificaciones(conectar_sit_hh, cr_timezone):
    st.title("📊 Panel de Certificaciones")
    hoja = conectar_sit_hh().worksheet("TCertificaciones")
    datos = hoja.get_all_values()

    if datos and len(datos) > 1:
        df = pd.DataFrame(datos[1:], columns=datos[0])
        df.columns = df.columns.str.strip().str.lower()

        # Validar columnas necesarias
        columnas_necesarias = {"fecha", "certificador", "ruta"}
        if not columnas_necesarias.issubset(df.columns):
            st.warning("⚠️ Las columnas necesarias no se encuentran en los datos.")
            return

        # Convertir tipos
        df["fecha"] = pd.to_datetime(df["fecha"], errors="coerce")
        df["duracion"] = pd.to_numeric(df["duracion"], errors="coerce")

        # Filtros
        rutas = sorted(df["ruta"].dropna().unique())
        certificadores = sorted(df["certificador"].dropna().unique())

        col1, col2 = st.columns(2)
        with col1:
            fecha_ini = st.date_input("Desde", value=datetime.now(cr_timezone).date())
        with col2:
            fecha_fin = st.date_input("Hasta", value=datetime.now(cr_timezone).date())

        ruta_sel = st.selectbox("Filtrar por Ruta", ["Todas"] + rutas)
        cert_sel = st.selectbox("Filtrar por Certificador", ["Todos"] + certificadores)

        df_filtrado = df[
            (df["fecha"].dt.date >= fecha_ini) & (df["fecha"].dt.date <= fecha_fin)
        ]
        if ruta_sel != "Todas":
            df_filtrado = df_filtrado[df_filtrado["ruta"] == ruta_sel]
        if cert_sel != "Todos":
            df_filtrado = df_filtrado[df_filtrado["certificador"] == cert_sel]

        # Mostrar registros filtrados
        st.subheader("📄 Registros Filtrados")
        st.dataframe(df_filtrado)

        # Certificaciones últimos 7 días
        ultima_semana = datetime.now(cr_timezone).date() - pd.Timedelta(days=7)
        df_ultimos_7 = df[df["fecha"].dt.date >= ultima_semana].copy()
        df_ultimos_7["fecha_str"] = df_ultimos_7["fecha"].dt.strftime("%Y-%m-%d")
        rutas_por_dia = df_ultimos_7.groupby("fecha_str").size().reset_index(name="Certificaciones")

        st.subheader("📅 Certificaciones en los últimos 7 días")
        st.bar_chart(rutas_por_dia.set_index("fecha_str"))

        # Gráfico circular por certificador
        st.subheader("🧑‍💼 Certificaciones por Usuario")
        cert_por_usuario = df_filtrado["certificador"].value_counts()
        st.pyplot(cert_por_usuario.plot.pie(autopct="%1.1f%%", figsize=(6, 6), ylabel="").figure)

        # Gráfico de barras por certificador
        resumen_certificadores = (
            df_filtrado.groupby("certificador")
            .size()
            .reset_index(name="Total certificaciones realizadas")
        )
        st.subheader("📊 Certificaciones por Usuario (Gráfico de Barras)")
        st.bar_chart(resumen_certificadores.set_index("certificador"))

       # 👤 Gráfico circular por Persona (con nombres normalizados)
        if "persona conteo" in df_filtrado.columns and df_filtrado["persona conteo"].notna().any():
            st.subheader("👤 Certificaciones por Persona")
        
            # Crear una copia limpia de los nombres
            personas_limpias = (
                df_filtrado["persona conteo"]
                .dropna()
                .astype(str)
                .str.strip()
                .str.title()
            )
        
            # Contar certificaciones por persona
            cert_por_persona = personas_limpias.value_counts()
        
            # Crear y mostrar gráfico circular
            st.pyplot(cert_por_persona.plot.pie(
                autopct="%1.1f%%",
                figsize=(6, 6),
                ylabel="",
                title="Distribución de certificaciones por persona"
            ).figure)
        # Gráfico circular por empresa
        if "empresa" in df_filtrado.columns:
            st.subheader("🏢 Certificaciones por Empresa")
            cert_por_empresa = df_filtrado["empresa"].value_counts().reset_index()
            cert_por_empresa.columns = ["Empresa", "Certificaciones"]
            st.pyplot(cert_por_empresa.set_index("Empresa").plot.pie(
                y="Certificaciones", autopct="%1.1f%%", figsize=(6, 6), ylabel=""
            ).figure)

        # Gráfico de barras por tipo de ruta
        if "tipo_ruta" in df_filtrado.columns:
            st.subheader("🛣️ Certificaciones por Tipo de Ruta")
            resumen_tipo = df_filtrado["tipo_ruta"].value_counts().reset_index()
            resumen_tipo.columns = ["Tipo de Ruta", "Certificaciones"]
            st.bar_chart(resumen_tipo.set_index("Tipo de Ruta"))

        # Exportar CSV
        csv = df_filtrado.to_csv(index=False).encode("utf-8")
        st.download_button("📥 Descargar CSV", csv, "certificaciones.csv", "text/csv")

        # Duración promedio por certificador
        st.subheader("📈 Duración promedio por certificador")
        resumen_duracion = df_filtrado.groupby("certificador")["duracion"].mean().reset_index()
        resumen_duracion["duracion"] = resumen_duracion["duracion"].round(2)
        st.dataframe(resumen_duracion)
        st.bar_chart(resumen_duracion.set_index("certificador"))

        # Total de certificaciones por ruta
        st.subheader("📊 Total de certificaciones por ruta")
        resumen_ruta = df_filtrado.groupby("ruta").size().reset_index(name="Certificaciones")
        st.dataframe(resumen_ruta)
        st.bar_chart(resumen_ruta.set_index("ruta"))
    else:
        st.warning("⚠️ No se encontraron registros en la hoja 'TCertificaciones'.")


