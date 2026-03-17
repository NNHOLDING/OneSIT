import streamlit as st

def mostrar_inicio():
    st.markdown("""
        <div style='text-align: center; margin-top: 60px;'>
            <h1 style='
                font-family: Arial Black, sans-serif;
                font-size: 80px;
                font-weight: 900;
                color: #0066cc;
                letter-spacing: 4px;
                text-shadow: 
                    -3px -3px 0 #ffffff,  
                    3px -3px 0 #ffffff,
                    -3px 3px 0 #ffffff,
                    3px 3px 0 #ffffff;'>
                WMS SIT
            </h1>
        </div>
    """, unsafe_allow_html=True)
