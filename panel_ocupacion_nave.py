import streamlit as st
import pandas as pd
import plotly.express as px


def mostrar_panel_ocupacion(libro):
    st.subheader("📊 Panel de ocupación de la nave")

    try:
        hoja = libro.worksheet("Ubicaciones")
        datos = hoja.get_all_values()
        encabezados = [col.strip() for col in datos[0]]
        df = pd.DataFrame(datos[1:], columns=encabezados)
    except Exception as e:
        st.error(f"No se pudo cargar la hoja Ubicaciones: {e}")
        return

    if "Pasillo" not in df.columns or "Estado" not in df.columns:
        st.warning("La hoja Ubicaciones no tiene las columnas necesarias.")
        return

    df["Pasillo"] = df["Pasillo"].str.strip().str.upper()
    df["Estado"] = df["Estado"].str.strip().str.lower()

    # 📊 Gráfico general de ocupación
    estado_global = df["Estado"].value_counts().reset_index()
    estado_global.columns = ["Estado", "Cantidad"]
    fig_global = px.pie(estado_global, names="Estado", values="Cantidad",
                        title="Ocupación total de la nave", color_discrete_sequence=["green", "red"])
    st.plotly_chart(fig_global, use_container_width=True)

    # 📊 Gráfico por pasillo
    ocupacion_por_pasillo = df.groupby(["Pasillo", "Estado"]).size().reset_index(name="Cantidad")
    fig_pasillos = px.bar(ocupacion_por_pasillo, x="Pasillo", y="Cantidad", color="Estado",
                          title="Ocupación por pasillo", barmode="stack",
                          color_discrete_map={"disponible": "green", "ocupado": "red"})
    st.plotly_chart(fig_pasillos, use_container_width=True)

