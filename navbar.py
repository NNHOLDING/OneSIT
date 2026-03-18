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
    .navbar label {
        color: white;
        font-weight: 600;
    }
    </style>
    """, unsafe_allow_html=True)

    opciones = [
        "🏠 Inicio",
        "📦 Registro de Handhelds",
        "🌡️ Registro de Temperatura",
        "🧪 Prueba de Ubicación",
        "📝 Gestión de Jornada",
        "🚨 Registro de Errores",
        "📋 Panel Administrativo",
        "📊 Panel de Certificaciones",
        "🕒 Productividad",
        "🏷️ Generación de LPNs",
        "📥 Almacenamiento LPN",
        "📦 Panel de Ocupación Nave",
        "🔍 Consulta de SKU",
        "📑 Reporte TRecibo",
        "🚫 Bloqueo de Ubicaciones",
        "🛠️ Mantenimiento",
        "📖 Ayuda",
        "📜 Bitácora",
        "📑 Reportes Generales"
    ]

    seleccion = st.selectbox("Menú principal", opciones, key="navbar")
    return seleccion
