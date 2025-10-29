import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches

estado_color = {
    "disponible": "green",
    "ocupado": "red",
    "reservado": "orange",
    "mantenimiento": "gray"
}

def mostrar_panel_visual(libro):
    st.subheader("🧱 Panel visual por pasillo")

    try:
        hoja = libro.worksheet("Ubicaciones")
        datos = hoja.get_all_values()
        encabezados = [col.strip() for col in datos[0]]
        df = pd.DataFrame(datos[1:], columns=encabezados)
    except Exception as e:
        st.error(f"No se pudo cargar la hoja Ubicaciones: {e}")
        return

    columnas_necesarias = ["Pasillo", "Tramo", "Nivel", "Posición", "Estado"]
    if not all(col in df.columns for col in columnas_necesarias):
        st.warning("Faltan columnas necesarias en la hoja.")
        return

    df["Pasillo"] = df["Pasillo"].str.strip().str.upper()
    df["Estado"] = df["Estado"].str.strip().str.lower()
    df["Tramo"] = df["Tramo"].astype(int)
    df["Nivel"] = df["Nivel"].astype(int)
    df["Posición"] = df["Posición"].astype(str).str.strip()

    pasillos = sorted(df["Pasillo"].unique())
    pasillo_seleccionado = st.selectbox("🧭 Selecciona el pasillo", pasillos)

    df_pasillo = df[df["Pasillo"] == pasillo_seleccionado]

    # Detectar tramos y niveles reales del pasillo
    tramos = sorted(df_pasillo["Tramo"].unique())
    niveles = sorted(df_pasillo["Nivel"].unique(), reverse=True)

    fig, ax = plt.subplots(figsize=(len(tramos) * 1.5, (len(niveles) + 1.5) * 1.5))

    for i, nivel in enumerate(niveles):
        for j, tramo in enumerate(tramos):
            celdas = df_pasillo[
                (df_pasillo["Tramo"] == tramo) &
                (df_pasillo["Nivel"] == nivel)
            ]

            if not celdas.empty:
                posiciones = []
                colores = []
                for _, fila in celdas.iterrows():
                    estado = fila["Estado"]
                    color = estado_color.get(estado, "black")
                    posiciones.append(fila["Posición"])
                    colores.append(color)
                texto = "\n".join(posiciones)
                color = colores[0] if len(set(colores)) == 1 else "gray"
            else:
                texto = ""
                color = "black"

            ax.add_patch(plt.Rectangle((j, i), 1, 1, color=color, edgecolor="white"))
            ax.text(j + 0.5, i + 0.5, texto, ha="center", va="center", fontsize
