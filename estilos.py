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

    /* Títulos principales */
    [data-testid="stAppViewContainer"] h1 {
        color: #000000 !important;
        font-weight: 700;
    }

    /* Subtítulos */
    [data-testid="stAppViewContainer"] h2,
    [data-testid="stAppViewContainer"] h3 {
        color: #006699 !important;
        font-weight: 600;
    }

    /* Labels y markdown en panel derecho */
    [data-testid="stAppViewContainer"] label,
    [data-testid="stAppViewContainer"] .stMarkdown {
        color: #000000 !important;
        font-size: 1.6em !important; /* Labels grandes */
        font-weight: 800 !important;
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
        background-color: transparent !important;
        border: none !important;
    }
    div[data-baseweb="select"] * {
        color: #c0c0c0 !important;
    }

    /* Opciones desplegables */
    ul[role="listbox"] {
        background-color: #ffffff !important;
        border: 1px solid #cccccc !important;
    }
    ul[role="listbox"] li {
        background-color: #ffffff !important;
        color: #c0c0c0 !important;
    }
    ul[role="listbox"] li:hover {
        background-color: #f2f2f2 !important;
        color: #c0c0c0 !important;
    }

    /* Tablas y grillas */
    [data-testid="stDataFrame"] table {
        background-color: #ffffff !important;
        color: #c0c0c0 !important;
    }
    [data-testid="stDataFrame"] th {
        background-color: #f2f2f2 !important;
        color: #c0c0c0 !important;
    }
    [data-testid="stDataFrame"] td {
        background-color: #ffffff !important;
        color: #c0c0c0 !important;
    }

    /* Cajas de texto (inputs) */
    input, textarea {
        background-color: transparent !important;
        color: #c0c0c0 !important;
        border: none !important;
        font-size: 1.2em !important; /* Texto más grande en inputs */
    }
    input:focus, textarea:focus {
        outline: none !important;
        border-bottom: 1px solid #006699 !important;
    }

    /* Navbar horizontal */
    .navbar {
        overflow: hidden;
        background-color: #006699;
        display: flex;
        justify-content: center;
        padding: 0;
        margin-bottom: 20px;
    }
    .navbar a, .dropdown .dropbtn {
        font-size: 16px;
        color: white;
        text-align: center;
        padding: 14px 20px;
        text-decoration: none;
        font-weight: 600;
    }
    .navbar a:hover, .dropdown:hover .dropbtn {
        background-color: #004466;
    }
    .dropdown {
        position: relative;
        display: inline-block;
    }
    .dropdown-content {
        display: none;
        position: absolute;
        background-color: #f9f9f9;
        min-width: 200px;
        box-shadow: 0px 8px 16px rgba(0,0,0,0.2);
        z-index: 1;
    }
    .dropdown-content a {
        color: #000000;
        padding: 12px 16px;
        text-decoration: none;
        display: block;
    }
    .dropdown-content a:hover {
        background-color: #ddd;
    }
    .dropdown:hover .dropdown-content {
        display: block;
    }
    </style>
    """, unsafe_allow_html=True)
