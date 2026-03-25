import streamlit as st
import datetime
import pytz

cr_timezone = pytz.timezone("America/Costa_Rica")

def panel_registro():
    st.title("🕒 Registro INS")

    # Bloque de estilo para fondo oscuro y texto claro
    st.markdown(
        """
        <style>
        .stSelectbox div[data-baseweb="select"] {
            background-color: #000000 !important;
            color: #FFFFFF !important;
            font-size: 18px !important;
        }
        .stSelectbox svg { fill: #FFFFFF !important; }
        .stSelectbox span { color: #FFFFFF !important; }
        </style>
        """,
        unsafe_allow_html=True
    )

    # Lista de horas en intervalos de 30 minutos
    horas = [f"{h:02d}:{m:02d}" for h in range(0,24) for m in (0,30)]
    hora_actual = datetime.datetime.now(cr_timezone).strftime("%H:%M")
    hora = st.selectbox("Hora", horas, index=horas.index(hora_actual))

    fecha = st.date_input("Fecha", datetime.datetime.now(cr_timezone).date())
    numero_evento = st.text_input("Número de evento")

    if st.button("Guardar"):
        st.success(f"✅ Guardado: {fecha}, {hora}, {numero_evento}")
