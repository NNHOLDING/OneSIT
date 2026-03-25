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

    ahora = datetime.datetime.now(cr_timezone)

    # Carrete dinámico: selectbox de horas y minutos
    horas = [f"{h:02d}" for h in range(0,24)]
    minutos = [f"{m:02d}" for m in range(0,60)]

    hora_sel = st.selectbox("Hora", horas, index=ahora.hour)
    minuto_sel = st.selectbox("Minutos", minutos, index=ahora.minute)

    # Combinar hora y minutos seleccionados
    hora_final = f"{hora_sel}:{minuto_sel}"

    fecha = st.date_input("Fecha", ahora.date())
    numero_evento = st.text_input("Número de evento")

    if st.button("Guardar"):
        st.success(f"✅ Guardado: {fecha}, {hora_final}, {numero_evento}")
