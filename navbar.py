import streamlit as st

def mostrar_navbar():
    st.markdown("""
    <style>
    .nav-container {
        display: flex;
        justify-content: center;
        background-color: #006699;
        padding: 10px;
        border-radius: 5px;
        margin-bottom: 20px;
    }
    .nav-button {
        background-color: #004466;
        color: white;
        font-weight: 600;
        border: none;
        padding: 8px 16px;
        margin: 0 5px;
        border-radius: 4px;
        cursor: pointer;
    }
    .nav-button:hover {
        background-color: #0088cc;
    }
    </style>
    """, unsafe_allow_html=True)

    # Definir las opciones del menú
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

    # Crear columnas para cada opción
    cols = st.columns(len(opciones))
    seleccion = None
    for i, opcion in enumerate(opciones):
        if cols[i].button(opcion, key=f"nav_{i}"):
            seleccion = opcion

    # Si no se ha hecho clic aún, por defecto mostrar Inicio
    if not seleccion:
        seleccion = "🏠 Inicio"

    return seleccion
