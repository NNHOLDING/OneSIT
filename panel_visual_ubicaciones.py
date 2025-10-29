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

    pasillos = sorted(df["Pasillo"].unique())
    pasillo_seleccionado = st.selectbox("🧭 Selecciona el pasillo", pasillos)

    df_pasillo = df[df["Pasillo"] == pasillo_seleccionado]

    # Determinar rango completo de tramos y niveles
    tramos = list(range(1, 8))  # 7 tramos estándar
    niveles = list(range(3, 0, -1))  # 3 niveles en orden descendente

    fig, ax = plt.subplots(figsize=(len(tramos), len(niveles)))

    for i, nivel in enumerate(niveles):
        for j, tramo in enumerate(tramos):
            celda = df_pasillo[
                (df_pasillo["Tramo"] == tramo) &
                (df_pasillo["Nivel"] == nivel)
            ]
            estado = celda["Estado"].values[0] if not celda.empty else "desconocido"
            color = estado_color.get(estado, "black")
            posicion = celda["Posición"].values[0] if not celda.empty else ""

            ax.add_patch(plt.Rectangle((j, i), 1, 1, color=color))
            ax.text(j + 0.5, i + 0.5, f"{posicion}", ha="center", va="center", fontsize=8, color="white")

    ax.set_xticks([x + 0.5 for x in range(len(tramos))])
    ax.set_xticklabels([f"T{x}" for x in tramos])
    ax.set_yticks([y + 0.5 for y in range(len(niveles))])
    ax.set_yticklabels([f"N{y}" for y in niveles])
    ax.set_xlim(0, len(tramos))
    ax.set_ylim(0, len(niveles))
    ax.set_title(f"Pasillo {pasillo_seleccionado}", fontsize=14)
    ax.axis("off")

    leyenda = [mpatches.Patch(color=color, label=estado.capitalize()) for estado, color in estado_color.items()]
    ax.legend(handles=leyenda, loc="lower center", bbox_to_anchor=(0.5, -0.1), ncol=len(leyenda))

    st.pyplot(fig)
