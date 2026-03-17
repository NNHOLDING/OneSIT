import streamlit as st

def aplicar_estilos():
    st.markdown("""
    <style>
    /* Fondo general */
    body {
        background-color: #e6e6e6;
        font-family: "Segoe UI", sans-serif;
        color: #333333;
    }

    /* Área principal */
    [data-testid="stAppViewContainer"] {
        background-color: #e6e6e6;
    }

    /* Barra superior */
    [data-testid="stHeader"] {
        background-color: #d9d9d9;
    }

    /* Sidebar */
    [data-testid="stSidebar"] {
        background-color: #002b36;
        color: #ffffff;
    }
    [data-testid="stSidebar"] h1,
    [data-testid="stSidebar"] h2,
    [data-testid="stSidebar"] h3,
    [data-testid="stSidebar"] label,
    [data-testid="stSidebar"] .stMarkdown {
        color: #ffffff !important;
    }

    /* Contenedor central */
    .main {
        background-color: #ffffff;
        border-radius: 8px;
        padding: 25px;
        box-shadow: 0px 2px 8px rgba(0,0,0,0.1);
    }

    /* Títulos */
    h1, h2, h3 {
        color: #006699;
        font-weight: 600;
    }

    /* Texto general */
    p, label, span, div {
        color: #333333;
    }

    /* Botones */
    .stButton>button {
        background-color: #006699;
        color: #ffffff !important;
        border-radius: 6px;
        padding: 8px 16px;
        font-weight: 500;
        border: none;
    }
    .stButton>button:hover {
        background-color: #004466;
    }

    /* Selectores y entradas */
    input, select, textarea {
        background-color: #ffffff !important;
        color: #333333 !important;
        border: 1px solid #cccccc !important;
        border-radius: 6px !important;
        padding: 6px 10px !important;
    }

    /* Forzar color del texto dentro de los selectores */
    .stSelectbox div[data-baseweb="select"] div {
        color: #333333 !important;
    }

    /* Tablas y dataframes */
    [data-testid="stDataFrame"], [data-testid="stTable"] {
        background-color: #ffffff !important;
        color: #333333 !important;
    }
    </style>
    """, unsafe_allow_html=True)
