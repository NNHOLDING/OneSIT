import streamlit as st
import datetime
import pytz

cr_timezone = pytz.timezone("America/Costa_Rica")

def panel_registro():
    st.title("🕒 Registro INS con reloj")

    # Hora actual
    hora_actual = datetime.datetime.now(cr_timezone).strftime("%H:%M:%S")

    # Reloj gráfico simple con HTML/CSS
    st.markdown(
        f"""
        <div style="
            background-color:#000000;
            color:#FFFFFF;
            font-size:32px;
            text-align:center;
            padding:20px;
            border-radius:10px;
            width:200px;
            margin:auto;
        ">
            {hora_actual}
        </div>
        """,
        unsafe_allow_html=True
    )

    # Aquí puedes mantener tus otros inputs
    fecha = st.date_input("Fecha", datetime.datetime.now(cr_timezone).date())
    numero_evento = st.text_input("Número de evento")