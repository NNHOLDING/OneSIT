import streamlit as st
from datetime import datetime
import pytz
import requests
from PIL import Image
from io import BytesIO

# 🔐 Importa tu función real de autenticación
from auth import validar_login

# Configuración inicial
st.set_page_config(
    page_title="Smart Intelligence Tools",
    page_icon="https://raw.githubusercontent.com/NNHOLDING/marcas_sit/main/NN25.ico",
    layout="centered"
)

cr_timezone = pytz.timezone("America/Costa_Rica")

# Estado de sesión
defaults = {
    "logueado_handheld": False,
    "rol_handheld": "",
    "nombre_empleado": "",
    "codigo_empleado": "",
    "confirmar_salida": False
}
for key, value in defaults.items():
    if key not in st.session_state:
        st.session_state[key] = value

# 🔐 Login
if not st.session_state.logueado_handheld:
    try:
        url_logo = "https://drive.google.com/uc?export=view&id=1CgMBkG3rUwWOE9OodfBN1Tjinrl0vMOh"
        response = requests.get(url_logo)
        if response.status_code == 200:
            image = Image.open(BytesIO(response.content))
            st.image(image, use_container_width=True)
        else:
            st.warning("⚠️ No se pudo cargar el logo.")
    except:
        st.warning("⚠️ Error al cargar el logo.")

    st.title("🔐 Smart Intelligence Tools")
    usuario = st.text_input("Usuario (Código o Admin)")
    contraseña = st.text_input("Contraseña", type="password")
    if st.button("Ingresar"):
        rol, nombre = validar_login(usuario, contraseña)
        if rol:
            st.session_state.logueado_handheld = True
            st.session_state.rol_handheld = rol
            st.session_state.nombre_empleado = nombre
            st.session_state.codigo_empleado = usuario
            st.success(f"Bienvenido, {nombre}")
            st.rerun()
        else:
            st.error("Credenciales incorrectas o usuario no válido.")

# 🧭 Interfaz principal
if st.session_state.logueado_handheld:
    # 🌐 Navbar horizontal
    st.markdown("""
    <style>
    .navbar {
        overflow: hidden;
        background-color: #2c3e50;
        font-family: Arial, sans-serif;
        margin-bottom: 30px;
    }
    .navbar a, .dropdown-btn {
        float: left;
        font-size: 16px;
        color: white;
        text-align: center;
        padding: 14px 20px;
        text-decoration: none;
        border: none;
        background: none;
        cursor: pointer;
    }
    .navbar a:hover, .dropdown:hover .dropdown-btn {
        background-color: #34495e;
    }
    .dropdown {
        float: left;
        overflow: hidden;
    }
    .dropdown-content {
        display: none;
        position: absolute;
        background-color: #ecf0f1;
        min-width: 180px;
        z-index: 1;
    }
    .dropdown-content a {
        float: none;
        color: #2c3e50;
        padding: 12px 16px;
        text-decoration: none;
        display: block;
        text-align: left;
    }
    .dropdown-content a:hover {
        background-color: #bdc3c7;
    }
    .dropdown:hover .dropdown-content {
        display: block;
    }
    </style>

    <div class="navbar">
      <a href="?modulo=registro">📦 Registro</a>
      <a href="?modulo=panel">📋 Panel</a>
      <div class="dropdown">
        <button class="dropdown-btn">🕒 Productividad ▼</button>
        <div class="dropdown-content">
          <a href="?modulo=alisto_form">Formulario Alisto</a>
          <a href="?modulo=alisto_panel">Panel Alisto</a>
        </div>
      </div>
      <a href="?modulo=jornada">📝 Jornada</a>
      <a href="?modulo=errores">🚨 Errores</a>
    </div>
    """, unsafe_allow_html=True)

    # 👤 Logo institucional
    st.markdown("""
        <div style='text-align: center;'>
            <img src='https://raw.githubusercontent.com/NNHOLDING/marcas_sit/main/28NN.PNG.jpg' width='250'>
        </div>
    """, unsafe_allow_html=True)

    # Detectar módulo activo
    modulo = st.query_params.get("modulo", "registro")

    # 🔀 Navegación por módulos
    if modulo == "registro":
        st.title("📦 Registro de Handhelds")
        st.write("Aquí va el formulario de registro.")

    elif modulo == "panel":
        st.title("📋 Panel Administrativo")
        st.write("Aquí va el panel con filtros y visualizaciones.")

    elif modulo == "alisto_form":
        st.title("📝 Formulario de Alisto")
        st.write("Aquí va el formulario de productividad para usuarios.")

    elif modulo == "alisto_panel":
        st.title("📊 Panel de Productividad")
        if st.session_state.rol_handheld == "admin":
            st.write("Aquí va el panel de productividad para administradores.")
        else:
            st.warning("⚠️ Acceso restringido: solo administradores pueden ver este panel.")

    elif modulo == "jornada":
        st.title("🕒 Gestión de Jornada")
        st.write("Aquí va la gestión de jornada laboral.")

    elif modulo == "errores":
        st.title("🚨 Registro de Errores")
        st.write("Aquí va el formulario para reportar errores.")

    # 🚪 Cierre de sesión
    st.markdown("---")
    st.markdown("### 🚪 Cerrar sesión")
    if st.button("Salir"):
        for key in defaults.keys():
            st.session_state[key] = False if key == "logueado_handheld" else ""
        st.rerun()

# 🧾 Footer institucional
st.markdown("""
    <hr style="margin-top: 50px; border: none; border-top: 1px solid #ccc;" />
    <div style="text-align: center; color: gray; font-size: 0.9em; margin-top: 20px;">
        NN HOLDING SOLUTIONS, Ever Be Better &copy; 2025, Todos los derechos reservados
    </div>
""", unsafe_allow_html=True)
