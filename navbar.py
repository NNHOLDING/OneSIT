import streamlit as st

def mostrar_navbar():
    st.markdown("""
    <style>
    .navbar {
        display: flex;
        justify-content: center;
        background-color: #006699;
        padding: 10px;
        margin-bottom: 20px;
    }
    .navbar div {
        margin: 0 10px;
    }
    .navbar label {
        color: white;
        font-weight: 600;
    }
    </style>
    """, unsafe_allow_html=True)

    col1, col2, col3, col4, col5 = st.columns(5)

    with col1:
        opcion_dispositivo = st.selectbox("Dispositivos", [
            "🏠 Inicio",
            "📦 Registro de Handhelds",
            "🌡️ Registro de Temperatura",
            "🧪 Prueba de Ubicación",
            "📝 Gestión de Jornada",
            "🚨 Registro de Errores"
        ], key="nav_dispositivos")

    with col2:
        opcion_admin = st.selectbox("Panel Administrativo", [
            "📋 Panel Administrativo",
            "📊 Panel de Certificaciones",
            "🕒 Productividad"
        ], key="nav_admin")

    with col3:
        opcion_almacen = st.selectbox("Almacenamiento", [
            "🏷️ Generación de LPNs",
            "📥 Almacenamiento LPN",
            "📦 Panel de Ocupación Nave",
            "🔍 Consulta de SKU",
            "📑 Reporte TRecibo"
        ], key="nav_almacen")

    with col4:
        opcion_extra = st.selectbox("Bloqueo / Mantenimiento", [
            "🚫 Bloqueo de Ubicaciones",
            "🛠️ Mantenimiento"
        ], key="nav_extra")

    with col5:
        opcion_misc = st.selectbox("Otros", [
            "📖 Ayuda",
            "📜 Bitácora",
            "📑 Reportes Generales"
        ], key="nav_misc")

    # Retornar la última opción seleccionada
    return opcion_dispositivo or opcion_admin or opcion_almacen or opcion_extra or opcion_misc
