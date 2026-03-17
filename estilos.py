import streamlit as st

def aplicar_estilos():
    st.markdown("""
    <style>
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

    /* Selectbox (BaseWeb) */
    div[data-baseweb="select"] {
        background-color: #ffffff !important;
        border: 1px solid #cccccc !important;
        border-radius: 6px !important;
    }
    div[data-baseweb="select"] div {
        color: #333333 !important;
    }
    div[data-baseweb="select"] input {
        color: #333333 !important;
        background-color: #ffffff !important;
    }

    /* Opciones desplegables */
    ul[role="listbox"] {
        background-color: #ffffff !important;
        border: 1px solid #cccccc !important;
    }
    ul[role="listbox"] li {
        background-color: #ffffff !important;
        color: #333333 !important;
    }
    ul[role="listbox"] li:hover {
        background-color: #f2f2f2 !important;
    }

    /* DataFrame / Tablas */
    [data-testid="stDataFrame"] {
        background-color: #ffffff !important;
        color: #333333 !important;
    }
    [data-testid="stDataFrame"] table {
        background-color: #ffffff !important;
        color: #333333 !important;
    }
    [data-testid="stDataFrame"] th {
        background-color: #f2f2f2 !important;
        color: #333333 !important;
    }
    [data-testid="stDataFrame"] td {
        background-color: #ffffff !important;
        color: #333333 !important;
    }
    </style>
    """, unsafe_allow_html=True)
