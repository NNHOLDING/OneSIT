import streamlit as st

def mostrar_inicio(usuario, codigo=None, rol=None):
    st.markdown(f"""
        <style>
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
            margin-bottom: 20px; /* separa la etiqueta de la imagen */
        }}
        .sega-text {{
            font-family: 'Arial Black', sans-serif;
            font-size: 80px;
            font-weight: 900;
            color: #0066cc;
            letter-spacing: 4px;
            text-transform: uppercase;
            text-align: center;
            margin-top: 40px; /* espacio suficiente para no chocar con la etiqueta */
            text-shadow: 
                -4px -4px 0 #ffffff,  
                 4px -4px 0 #ffffff,
                -4px  4px 0 #ffffff,
                 4px  4px 0 #ffffff,
                 0px  0px 8px #000000;
        }}
        </style>
        <div class="user-label">
            👤 {usuario} <br>
            🆔 {codigo if codigo else ""} <br>
            🎯 {rol if rol else ""}
        </div>
        <div class="sega-text">WMS SIT</div>
    """, unsafe_allow_html=True)

    # Imagen desde GitHub (enlace raw)
    st.image(
        "https://raw.githubusercontent.com/NNHOLDING/OneSIT/main/electric-stacker-4-1-1024x683.jpg",
        width=700
    )
