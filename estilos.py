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

    /* Panel derecho (área principal) */
    [data-testid="stAppViewContainer"] {
        background-color: #d0d0d0 !important; /* Gris medio, más sobrio */
    }

    /* Contenedor central dentro del panel */
    .main {
        background-color: #f5f5f5 !important; /* Gris claro suave */
        border-radius: 8px;
        padding: 25px;
        box-shadow: 0px 2px 8px rgba(0,0,0,0.1);
    }

    /* Títulos */
    h1, h2, h3 {
        color: #006699; /* Azul corporativo */
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
    </style>
    """, unsafe_allow_html=True)
