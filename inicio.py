import streamlit as st
from datetime import datetime

def mostrar_inicio(usuario, codigo=None, rol=None):
    # Obtener fecha actual
    fecha_actual = datetime.now().strftime("%d/%m/%Y")

    st.markdown(f"""
        <style>
        .date-label {{
            font-family: Arial, sans-serif;
            font-size: 20px;
            font-weight: bold;
            color: #333333;
            background-color: #d0d0d0; /* mismo color que el footer */
            padding: 8px 16px;
            border-radius: 8px;
            box-shadow: 2px 2px 6px rgba(0,0,0,0.2);
            text-align: left;
            float: left;
            margin-bottom: 20px;
        }}
        .user-label {{
            font-family: Arial, sans-serif;
            font-size: 20px;
            font-weight: bold;
            color: #333333;
            background-color: #d0d0d0; /* mismo color que el footer */
            padding: 8px 16px;
            border-radius: 8px;
            box-shadow: 2px 2px 6px rgba(0,0,0,0.2);
            text-align: right;
            float: right;
            margin-bottom: 20px;
        }}
        .clearfix {{
            clear: both;
        }}
        .sega-text {{
            font-family: 'Arial Black', sans-serif;
            font-size: 80px;
            font-weight: 900;
            color: #0066cc;
            letter-spacing: 4px;
            text-transform: uppercase;
            text-align: center;
            margin-top: 40px;
            text-shadow: 
                -4px -4px 0 #ffffff,  
                 4px -4px 0 #ffffff,
                -4px  4px 0 #ffffff,
                 4px  4px 0 #ffffff,
                 0px  0px 8px #000000;
        }}
        </style>
        <div class="date-label">
            📅 {fecha_actual}
        </div>
        <div class="user-label">
            👤 {usuario} <br>
            🆔 {codigo if codigo else ""} <br>
            🎯 {rol if rol else ""}
        </div>
        <div class="clearfix"></div>
        <div class="sega-text">WMS SIT</div>
    """, unsafe_allow_html=True)

    # Imagen desde GitHub (enlace raw)
    st.image(
        "https://raw.githubusercontent.com/NNHOLDING/OneSIT/main/electric-stacker-4-1-1024x683.jpg",
        width=800
    )
