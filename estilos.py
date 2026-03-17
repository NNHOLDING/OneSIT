import streamlit as st

def aplicar_estilos():
    st.markdown("""
    <style>
    /* Sidebar corporativo */
    [data-testid="stSidebar"] {
        background-color: #002b36 !important; /* Azul corporativo */
        color: #ffffff !important;
    }
    [data-testid="stSidebar"] h1,
    [data-testid="stSidebar"] h2,
    [data-testid="stSidebar"] h3,
    [data-testid="stSidebar"] label,
    [data-testid="stSidebar"] .stMarkdown {
        color: #ffffff !important;
    }

    /* Panel derecho */
    [data-testid="stAppViewContainer"] {
        background-color: #d0d0d0 !important; /* Gris medio */
    }

    /* Contenedor central */
    .main {
        background-color: #f5f5f5 !important; /* Gris claro */
        border-radius: 8px;
        padding: 25px;
        box-shadow: 0px 2px 8px rgba(0,0,0,0.1);
    }

    /* Títulos */
    h1, h2, h3 {
        color: #006699;
        font-weight: 600;
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

    /* Selectores */
    div[data-baseweb="select"] {
        background-color: #ffffff !important;
        border: 1px solid #cccccc !important;
        border-radius: 6px !important;
    }
    div[data-baseweb="select"] * {
        color: #c0c0c0 !important; /* Fuente plata */
    }

    /* Opciones desplegables al abrir selector */
    ul[role="listbox"] {
        background-color: #ffffff !important;
        border: 1px solid #cccccc !important;
    }
    ul[role="listbox"] li {
        background-color: #ffffff !important;
        color: #c0c0c0 !important; /* Fuente plata en todas las opciones */
    }
    ul[role="listbox"] li:hover {
        background-color: #f2f2f2 !important;
        color: #c0c0c0 !important;
    }

    /* Tablas y grillas */
    [data-testid="stDataFrame"] table {
        background-color: #ffffff !important;
        color: #c0c0c0 !important; /* Fuente plata */
    }
    [data-testid="stDataFrame"] th {
        background-color: #f2f2f2 !important;
        color: #c0c0c0 !important;
    }
    [data-testid="stDataFrame"] td {
        background-color: #ffffff !important;
        color: #c0c0c0 !important;
    }
    </style>
    """, unsafe_allow_html=True)
