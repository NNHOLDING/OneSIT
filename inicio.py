import streamlit as st

def mostrar_inicio():
    st.markdown("""
        <div style='text-align: center; margin-top: 50px;'>
            <h1 style='
                font-family: Arial Black, sans-serif;
                font-size: 72px;
                font-weight: 900;
                color: #006699;
                text-shadow: 3px 3px 0px #ffffff, 
                             -3px -3px 0px #ffffff,
                             3px -3px 0px #ffffff,
                             -3px 3px 0px #ffffff;'>
                WMS SIT
            </h1>
        </div>
    """, unsafe_allow_html=True)
