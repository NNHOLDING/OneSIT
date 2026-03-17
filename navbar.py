import streamlit as st

def mostrar_navbar():
    # Inicializar selección
    if "modulo_seleccionado" not in st.session_state:
        st.session_state.modulo_seleccionado = "Inicio"

    # Estilos del navbar
    st.markdown("""
    <style>
    .navbar {
        overflow: hidden;
        background-color: #006699;
        display: flex;
        justify-content: center;
        padding: 0;
        margin-bottom: 20px;
    }
    .dropdown {
        position: relative;
        display: inline-block;
    }
    .dropbtn {
        font-size: 16px;
        color: white;
        padding: 14px 20px;
        border: none;
        background: none;
        font-weight: 600;
        cursor: pointer;
    }
    .dropdown-content {
        display: none;
        position: absolute;
        background-color: #f9f9f9;
        min-width: 220px;
        box-shadow: 0px 8px 16px rgba(0,0,0,0.2);
        z-index: 1;
    }
    .dropdown-content button {
        background: none;
        border: none;
        color: #000;
        padding: 12px 16px;
        text-align: left;
        width: 100%;
        cursor: pointer;
    }
    .dropdown-content button:hover {
        background-color: #ddd;
    }
    .dropdown:hover .dropdown-content {
        display: block;
    }
    </style>
    """, unsafe_allow_html=True)

    # Navbar
    st.markdown('<div class="navbar">', unsafe_allow_html=True)

    # Inicio
    if st.button("Inicio", key="nav_inicio"):
        st.session_state.modulo_seleccionado = "Inicio"

    # Dropdown Dispositivos
    st.markdown('<div class="dropdown"><button class="dropbtn">Dispositivos ▼</button><div class="dropdown-content">', unsafe_allow_html=True)
    for i, mod in enumerate([
        "📦 Registro de Handhelds",
        "🌡️ Registro de Temperatura",
        "🧪 Prueba de registro",
        "📝 Registro de Jornadas",
        "🚨 Registro de Errores"
    ]):
        if st.button(mod, key=f"disp_{i}"):
            st.session_state.modulo_seleccionado = mod
    st.markdown('</div></div>', unsafe_allow_html=True)

    # Dropdown Panel Administrativo
    st.markdown('<div class="dropdown"><button class="dropbtn">Panel Administrativo ▼</button><div class="dropdown-content">', unsafe_allow_html=True)
    for i, mod in enumerate([
        "📋 Panel Administrativo",
        "📊 Panel de Certificaciones",
        "📝 Gestión de Jornada",
        "🕒 Productividad"
    ]):
        if st.button(mod, key=f"admin_{i}"):
            st.session_state.modulo_seleccionado = mod
    st.markdown('</div></div>', unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)

    # Mostrar módulo seleccionado
    st.write(f"📌 Módulo actual: {st.session_state.modulo_seleccionado}")
