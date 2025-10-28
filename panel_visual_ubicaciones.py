import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches

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

    # Normalizar columnas
    for col in ["Pasillo", "Tramo", "Nivel", "Posición", "Estado"]:
        if col not in df.columns:
            st.warning(f"Falta la columna '{col}' en la hoja.")
            return

    df["Pasillo"] = df["Pasillo"].str.strip().str.upper()
    df["Estado"] = df["Estado"].str.strip().str.lower()

    pasillos = sorted(df["Pasillo"].unique())
    pasillo_seleccionado = st.selectbox("🧭 Selecciona el pasillo", pasillos)

    df_pasillo = df[df["Pasillo"] == pasillo_seleccionado]

    # Crear matriz por tramo y nivel
    tramos = sorted(df_pasillo["Tramo"].astype(int).unique())
    niveles = sorted(df_pasillo["Nivel"].astype(int).unique(), reverse=True)

    fig, ax = plt.subplots(figsize=(len(tramos), len(niveles)))
    for i, nivel in enumerate(niveles):
        for j, tramo in enumerate(tramos):
            celda = df_pasillo[
                (df_pasillo["Tramo"].astype(int) == tramo) &
                (df_pasillo["Nivel"].astype(int) == nivel)
            ]
            estado = celda["Estado"].values[0] if not celda.empty else "desconocido"
            color = "green" if estado == "disponible" else "red"
            ax.add_patch(plt.Rectangle((j, i), 1, 1, color=color))
            texto = celda["Posición"].values[0] if not celda.empty else ""
            ax.text(j + 0.5, i + 0.5, texto, ha="center", va="center", fontsize=8, color="white")

    ax.set_xticks([i + 0.5 for i in range(len(tramos))])
    ax.set_xticklabels([f"T{t}" for t in tramos])
    ax.set_yticks([i + 0.5 for i in range(len(niveles))])
    ax.set_yticklabels([f"N{n}" for n in niveles])
    ax.set_xlim(0, len(tramos))
    ax.set_ylim(0, len(niveles))
    ax.set_title(f"Pasillo {pasillo_seleccionado}", fontsize=14)
    ax.axis("off")

    leyenda = [mpatches.Patch(color="green", label="Disponible"),
               mpatches.Patch(color="red", label="Ocupado")]
    ax.legend(handles=leyenda, loc="lower center", bbox_to_anchor=(0.5, -0.1), ncol=2)

    st.pyplot(fig)