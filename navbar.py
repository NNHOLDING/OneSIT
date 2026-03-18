import streamlit as st

def mostrar_navbar():
    st.markdown("""
    <style>
    .navbar {
        display: flex;
        justify-content: space-around;
        background-color: #006699;
        padding: 10px;
        border-radius: 5px;
        margin-bottom: 20px;
    }
    .navbar h4 {
        color: white;
        margin: 0;
        font-weight: 600;
    }
    </style>
    """, unsafe_allow_html=True)

    # Primer nivel: secciones
    seccion = st.radio(
        "Secciones",
        ["Dispositivos", "Administrativo", "Almacenamiento", "Otros"],
        horizontal=True,
        key="nav_seccion"
    )

    # Segundo nivel: opciones según sección
    if seccion == "Dispositivos":
        opcion = st.selectbox("Opciones", [
            "🏠 Inicio",
            "📦 Registro de Handhelds",
            "🌡️ Registro de Temperatura",
            "🧪 Prueba de Ubicación",
            "📝 Gestión de Jornada",
            "🚨 Registro de Errores"
        ], key="nav_dispositivos")

    elif seccion == "Administrativo":
        opcion = st.selectbox("Opciones", [
            "📋 Panel Administrativo",
            "📊 Panel de Certificaciones",
            "🕒 Productividad"
        ], key="nav_admin")

    elif seccion == "Almacenamiento":
        opcion = st.selectbox("Opciones", [
            "🏷️ Generación de LPNs",
            "📥 Almacenamiento LPN",
            "📦 Panel de Ocupación Nave",
            "🔍 Consulta de SKU",
            "📑 Reporte TRecibo"
        ], key="nav_almacen")

    else:  # Otros
        opcion = st.selectbox("Opciones", [
            "🚫 Bloqueo de Ubicaciones",
            "🛠️ Mantenimiento",
            "📖 Ayuda",
            "📜 Bitácora",
            "📑 Reportes Generales"
        ], key="nav_misc")

    return opcion
