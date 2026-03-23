import streamlit as st
import pandas as pd
import pytz
import requests
from PIL import Image
from io import BytesIO

# Módulos personalizados
from auth import validar_login
from google_sheets import conectar_sit_hh
from registro import registrar_handheld
from jornadas import mostrar_jornadas
from registro_jornada import gestionar_jornada
from modulo_alisto import mostrar_formulario_alisto
from panel_productividad_alisto import mostrar_panel_alisto
from registro_errores import mostrar_formulario_errores
from modulo_temperatura import mostrar_formulario_temperatura
from panel_administrativo import mostrar_panel_administrativo
from panel_certificaciones import mostrar_panel_certificaciones
from prueba_ubicacion import mostrar_prueba_ubicacion
from calculos_jornada import procesar_jornadas
from modulo_lpn import mostrar_formulario_lpn
from modulo_almacenamiento_lpn import mostrar_formulario_almacenamiento_lpn
from panel_visual_ubicaciones import mostrar_panel_visual
from panel_ocupacion_nave import mostrar_panel_ocupacion
from modulo_bloqueo_ubicaciones import mostrar_formulario_bloqueo
from modulo_consulta_sku import mostrar_consulta_sku
from modulo_reporte import mostrar_reporte
from defaults import defaults
from estilos import aplicar_estilos
from bitacora import registrar_log
from inicio import mostrar_inicio
from navbar import mostrar_navbar
import streamlit as st
from usuario_info import mostrar_usuario_info
from footer import mostrar_footer
from cerrar_sesion import cerrar_sesion



# Configuración de página
st.set_page_config(
    page_title="Smart Intelligence Tools",
    page_icon="https://github.com/NNHOLDING/marcas_sit/raw/main/sitfavicon.ico",
    layout="centered"
)
# Aplica estilos corporativos
aplicar_estilos()
 
# Mostrar navbar y obtener selección (devuelve un string)
# modulo = mostrar_navbar()

cr_timezone = pytz.timezone("America/Costa_Rica")

# Verificar estado de mantenimiento
def obtener_estado_mantenimiento():
    try:
        libro = conectar_sit_hh()
        hojas_disponibles = [hoja.title for hoja in libro.worksheets()]
        if "configuracion" not in hojas_disponibles:
            return "inactivo"
        hoja_config = libro.worksheet("configuracion")
        datos = hoja_config.get_all_values()
        config_df = pd.DataFrame(datos[1:], columns=datos[0])
        estado = config_df.loc[config_df["clave"] == "mantenimiento", "valor"].values
        return estado[0].strip().lower() if len(estado) > 0 else "inactivo"
    except Exception:
        return "inactivo"

# Mostrar aviso de mantenimiento
if obtener_estado_mantenimiento() == "activo":
    st.markdown("""
        <div style='text-align: center; padding: 40px; background-color: #fff3cd; border: 1px solid #ffeeba; border-radius: 10px; color: #000000;'>
            <h2 style='color: #000000;'>🛠️ Sitio en mantenimiento</h2>
            <p style='color: #000000;'>Estamos realizando mejoras. Por favor, vuelve más tarde.</p>
        </div>
    """, unsafe_allow_html=True)
    st.stop()

# Inicializar sesión
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

            # ✅ Registrar login en LogEnvios SOLO si el login fue exitoso
            registrar_log(usuario, nombre, "Login", "Inicio de sesión")

            st.rerun()
        else:
            st.error("Credenciales incorrectas o usuario no válido.")
# 🧭 Interfaz principal
if st.session_state.logueado_handheld:
    st.markdown("""
        <div style='text-align: center;'>
        <img src='https://raw.githubusercontent.com/NNHOLDING/marcas_sit/main/28NN.PNG.jpg' width='250'>
        </div>
    """, unsafe_allow_html=True)

    # Aquí seguiría tu lógica de módulos

    modulos_admin = [
        "🏠 Inicio",
        "📦 Registro de Handhelds",
        "📋 Panel Administrativo",
        "📊 Panel de Certificaciones",
        "🕒 Productividad",
        "📝 Gestión de Jornada",
        "🚨 Registro de Errores",
        "🌡️ Registro de Temperatura",
        "🧪 Prueba de Ubicación",
        "🏷️ Generación de LPNs",
        "📥 Almacenamiento LPN ",
        "📦 Panel de Ocupación Nave",
        "🚫 Bloqueo de Ubicaciones",
        "🔍 Consulta de SKU",
        "📑 Reporte TRecibo",
    ]
    modulos_usuario = [
        "🏠 Inicio",
        "📦 Registro de Handhelds",
        "🕒 Productividad",
        "📝 Gestión de Jornada",
        "🌡️ Registro de Temperatura",
        "🏷️ Generación de LPNs",
        "🧪 Prueba de Ubicación",
        "📑 Reporte TRecibo",
    ]
    modulos_supervisor = [
        "🏠 Inicio",
        "📦 Registro de Handhelds",
        "🕒 Productividad",
        "📝 Gestión de Jornada",
        "🚨 Registro de Errores",
        "🏷️ Generación de LPNs",
        "📑 Reporte TRecibo",
    ]

    # Selección dinámica según rol
    rol = st.session_state.rol_handheld
    if rol == "admin":
        opciones_menu = modulos_admin
    elif rol == "supervisor":
        opciones_menu = modulos_supervisor
    else:
        opciones_menu = modulos_usuario


    modulo = st.sidebar.selectbox("🧩 Selecciona el módulo", opciones_menu)
    if modulo == "🏠 Inicio":
        # mostrar_inicio()
        mostrar_inicio(st.session_state.nombre_empleado)
        mostrar_usuario_info()  # 👈 Aquí se muestra el panel con el usuario logeado

    if modulo == "📦 Registro de Handhelds":
        st.title("📦 Registro de Handhelds")
        st.text_input("Nombre", value=st.session_state.nombre_empleado, disabled=True)
        if st.session_state.rol_handheld != "admin":
            st.text_input("Código", value=st.session_state.codigo_empleado, disabled=True)
        equipos = [f"Equipo {i}" for i in range(1, 25)]
        equipo = st.selectbox("Selecciona el equipo", equipos)
        col1, col2 = st.columns(2)
        with col1:
            if st.button("📌 Guardar Entrega"):
                registrar_handheld(st.session_state.codigo_empleado, st.session_state.nombre_empleado, equipo, "entrega")
        with col2:
            if st.button("✅ Guardar Devolución"):
                registrar_handheld(st.session_state.codigo_empleado, st.session_state.nombre_empleado, equipo, "devolucion")

    elif modulo == "📋 Panel Administrativo":
        if st.session_state.rol_handheld != "admin":
            st.error("⛔ No tienes permisos para acceder a este módulo.")
        else:
            mostrar_panel_administrativo(conectar_sit_hh, cr_timezone)

    elif modulo == "🕒 Productividad":
        if st.session_state.rol_handheld == "admin":
            mostrar_panel_alisto(conectar_sit_hh)
        else:
            mostrar_formulario_alisto(
                GOOGLE_SHEET_ID="1o-GozoYaU_4Ra2KgX05Yi4biDV9zcd6BGdqOdSxKAv0",
                service_account_info=st.secrets["gcp_service_account"],
                nombre_empleado=st.session_state.nombre_empleado,
                codigo_empleado=st.session_state.codigo_empleado
            )

    elif modulo == "📊 Panel de Certificaciones":
        mostrar_panel_certificaciones(conectar_sit_hh, cr_timezone)

    elif modulo == "📝 Gestión de Jornada":
        gestionar_jornada(conectar_sit_hh, st.session_state.nombre_empleado)
        if st.session_state.rol_handheld == "admin":
            st.markdown("---")
            mostrar_jornadas(conectar_sit_hh)
            if st.button("⚙️ Procesar jornadas y calcular extras"):
                procesar_jornadas(conectar_sit_hh)
                st.success("✅ Cálculos completados y hoja actualizada.")

    elif modulo == "🚨 Registro de Errores":
        mostrar_formulario_errores()

    elif modulo == "🌡️ Registro de Temperatura":
        mostrar_formulario_temperatura(conectar_sit_hh, cr_timezone)

    elif modulo == "🧪 Prueba de Ubicación":
        mostrar_prueba_ubicacion()

    elif modulo == "🏷️ Generación de LPNs":
        mostrar_formulario_lpn()

    elif modulo == "📥 Almacenamiento LPN ":
        mostrar_formulario_almacenamiento_lpn()
        st.markdown("---")
        st.subheader("🧭 Opciones avanzadas")
        mostrar_panel_visual(conectar_sit_hh())

    elif modulo == "📦 Panel de Ocupación Nave":
        mostrar_panel_ocupacion(conectar_sit_hh())

    elif modulo == "🚫 Bloqueo de Ubicaciones":
        mostrar_formulario_bloqueo(conectar_sit_hh())

    elif modulo == "🔍 Consulta de SKU":
        mostrar_consulta_sku(conectar_sit_hh)

    elif modulo == "📑 Reporte TRecibo":
        mostrar_reporte(conectar_sit_hh)

   # 🚪 Cierre de sesión
    st.markdown("---")
    st.markdown("### 🚪 Cerrar sesión")
    if st.button("Salir", key="boton_salir"):
        cerrar_sesion()


# 🧾 Footer institucional
mostrar_footer()
