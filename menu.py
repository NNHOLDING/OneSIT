import streamlit as st

def mostrar_menu(opciones):
    st.markdown("""
        <style>
        /* Botón hamburger */
        .hamburger {
            position: fixed;
            top: 15px;
            left: 15px;
            width: 30px;
            height: 25px;
            cursor: pointer;
            z-index: 1000;
        }
        .hamburger div {
            background-color: #006699;
            height: 4px;
            margin: 5px 0;
            border-radius: 2px;
        }

        /* Menú lateral oculto */
        .menu {
            position: fixed;
            top: 0;
            left: -250px; /* oculto */
            width: 250px;
            height: 100%;
            background-color: #002b36;
            color: white;
            padding: 20px;
            transition: left 0.3s ease;
            z-index: 999;
        }
        .menu.show {
            left: 0; /* visible */
        }
        .menu a {
            display: block;
            color: white;
            text-decoration: none;
            margin: 15px 0;
            font-weight: 600;
        }
        .menu a:hover {
            background-color: #004466;
            padding: 5px;
            border-radius: 4px;
        }
        </style>

        <div class="hamburger" onclick="document.querySelector('.menu').classList.toggle('show')">
            <div></div>
            <div></div>
            <div></div>
        </div>
        <div class="menu">
    """, unsafe_allow_html=True)

    # Renderizar opciones dinámicamente
    for opcion in opciones:
        st.markdown(f"<a href='#{opcion}'>{opcion}</a>", unsafe_allow_html=True)

    st.markdown("</div>", unsafe_allow_html=True)