import streamlit as st

def mostrar_inicio():
    st.markdown("""
        <style>
        .sega-text {
            font-family: 'Arial Black', sans-serif;
            font-size: 80px;
            font-weight: 900;
            color: #0066cc;
            letter-spacing: 4px;
            text-transform: uppercase;
            text-align: center;
            margin-top: 60px;
            /* Borde blanco grueso alrededor */
            text-shadow: 
                -4px -4px 0 #ffffff,  
                 4px -4px 0 #ffffff,
                -4px  4px 0 #ffffff,
                 4px  4px 0 #ffffff,
                 0px  0px 8px #000000;
        }
        </style>
        <div class="sega-text">WMS SIT</div>
    """, unsafe_allow_html=True)
