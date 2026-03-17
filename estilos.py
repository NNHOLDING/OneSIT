import streamlit as st

def aplicar_estilos():
    st.markdown("""
    <style>
    /* Sidebar corporativo */
    [data-testid="stSidebar"] {
        background-color: #002b36 !important; /* Azul oscuro corporativo */
        color: #ffffff !important;
    }

    [data-testid="stSidebar"] h1,
    [data-testid="stSidebar"] h2,
    [data-testid="stSidebar"] h3,
    [data-testid="stSidebar"] label,
    [data-testid="stSidebar"] .stMarkdown {
        color: #ffffff !important;
    }
    </style>
    """, unsafe_allow_html=True)
