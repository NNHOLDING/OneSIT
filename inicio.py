import streamlit as st

def mostrar_inicio(usuario=" "):
    st.markdown(f"""
        <style>
        .user-label {{
            position: absolute;
            top: 20px;
            right: 40px;
            font-family: Arial, sans-serif;
            font-size: 20px;
            font-weight: bold;
            color: #333333;
            background-color: #f0f0f0;
            padding: 8px 16px;
            border-radius: 8px;
            box-shadow: 2px 2px 6px rgba(0,0,0,0.2);
        }}
        .sega-text {{
            font-family: 'Arial Black', sans-serif;
            font-size: 80px;
            font-weight: 900;
            color: #0066cc;
            letter-spacing: 4px;
            text-transform: uppercase;
            text-align: center;
            margin-top: 100px; /* más espacio para que no se superponga con la label */
            text-shadow: 
                -4px -4px 0 #ffffff,  
                 4px -4px 0 #ffffff,
                -4px  4px 0 #ffffff,
                 4px  4px 0 #ffffff,
                 0px  0px 8px #000000;
        }}
        </style>
        <div class="user-label">👤 {usuario}</div>
        <div class="sega-text">WMS SIT</div>
    """, unsafe_allow_html=True)

    # Imagen desde GitHub (enlace raw)
    st.image("https://raw.githubusercontent.com/NNHOLDING/OneSIT/main/electric-stacker-4-1-1024x683.jpg", width=600)
