import streamlit as st

def mostrar_navbar(opciones_menu):
    st.markdown("""
    <style>
    .navbar {
        background-color: #006699;
        padding: 10px;
        border-radius: 5px;
        margin-bottom: 20px;
    }
    .navbar label {
        color: white;
        font-weight: 600;
    }
    </style>
    """, unsafe_allow_html=True)

    # Menú horizontal con las opciones que recibe según rol
    seleccion = st.radio(
        "🧩 Selecciona el módulo",
        opciones_menu,
        horizontal=True,
        key="navbar"
    )
    return seleccion
