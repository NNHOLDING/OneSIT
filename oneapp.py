import streamlit as st
import pandas as pd
from datetime import datetime
import pytz
import requests
from PIL import Image
from io import BytesIO

from auth import validar_login
from google_sheets import conectar_sit_hh
from registro import registrar_handheld
from jornadas import mostrar_jornadas
from registro_jornada import gestionar_jornada
from modulo_alisto import mostrar_formulario_alisto
from panel_productividad_alisto import mostrar_panel_alisto
from registro_errores import mostrar_formulario_errores

st.set_page_config(
    page_title="Smart Intelligence Tools",
    page_icon="https://raw.githubusercontent.com/NNHOLDING/marcas_sit/main/NN25.ico",
    layout="centered"
)

cr_timezone = pytz.timezone("America/Costa_Rica")

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

# 🧭 Interfaz principal post-login
if st.session_state.logueado_handheld:
    # 🌐 Menú horizontal
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

    # Detectar módulo activo
    modulo = st.query_params.get("modulo", "registro")

    # Mostrar contenido según el módulo
    if modulo == "registro":
        st.title("📦 Registro de Handhelds")
        st.text_input("Nombre", value=st.session_state.nombre_empleado, disabled=True)
        if st.session_state.rol_handheld != "admin":
            st.text_input("Código", value=st.session_state.codigo_empleado, disabled=True)

        equipos = [f"Equipo {i}" for i in range(1, 25)]
        equipo = st.selectbox("Selecciona el equipo", equipos)

        col1, col2 = st.columns(2)
        with col1:
            if st.button("📌 Guardar Entrega"):
                registrar_handheld(
                    st.session_state.codigo_empleado,
                    st.session_state.nombre_empleado,
                    equipo, "entrega"
                )
        with col2:
            if st.button("✅ Guardar Devolución"):
                registrar_handheld(
                    st.session_state.codigo_empleado,
                    st.session_state.nombre_empleado,
                    equipo, "devolucion"
                )

    elif modulo == "panel":
        st.title("📋 Panel Administrativo")
        hoja = conectar_sit_hh().worksheet("HH")
        datos = hoja.get_all_values()
        if datos and len(datos[0]) > 0:
            df = pd.DataFrame(datos[1:], columns=datos[0])
            df.columns = df.columns.str.strip().str.lower()
            df["fecha"] = pd.to_datetime(df["fecha"], errors="coerce")

            usuarios = sorted(df["nombre"].dropna().unique())
            fecha_ini = st.date_input("Desde", value=datetime.now(cr_timezone).date())
            fecha_fin = st.date_input("Hasta", value=datetime.now(cr_timezone).date())
            usuario_sel = st.selectbox("Filtrar por Usuario", ["Todos"] + usuarios)

            df_filtrado = df[
                (df["fecha"].dt.date >= fecha_ini) &
                (df["fecha"].dt.date <= fecha_fin)
            ]
            if usuario_sel != "Todos":
                df_filtrado = df_filtrado[df_filtrado["nombre"] == usuario_sel]

            st.subheader("📑 Registros")
            st.dataframe(df_filtrado)

            hoy = datetime.now(cr_timezone).date()
            if "estatus" in df.columns:
                entregados_hoy = df[
                    (df["fecha"].dt.date == hoy) &
                    (df["estatus"].str.lower() == "entregado")
                ]
                devueltos_hoy = df[
                    (df["fecha"].dt.date == hoy) &
                    (df["estatus"].str.lower() == "devuelto")
                ]

                st.subheader("✅ Registros Entregados Hoy")
                st.dataframe(entregados_hoy)

                st.subheader("📤 Registros Devueltos Hoy")
                st.dataframe(devueltos_hoy)

                st.markdown("### 📊 Resumen de Movimientos Hoy")
                col1, col2 = st.columns(2)
                with col1:
                    st.metric("Entregados", len(entregados_hoy))
                with col2:
                    st.metric("Devueltos", len(devueltos_hoy))
            else:
                st.info("ℹ️ No se encontró la columna 'estatus' para mostrar entregas y devoluciones de hoy.")
            csv = df_filtrado.to_csv(index=False).encode("utf-8")
            st.download_button("📥 Descargar CSV", csv, "handhelds.csv", "text/csv")

            st.subheader("📊 Actividad por Usuario")
            resumen = df_filtrado.groupby("nombre").size().reset_index(name="Registros")
            st.dataframe(resumen)
            st.bar_chart(resumen.set_index("nombre"))

            st.subheader("🔧 Actividad por Equipo")
            resumen_eq = df_filtrado.groupby("equipo").size().reset_index(name="Movimientos")
            st.dataframe(resumen_eq)
            st.bar_chart(resumen_eq.set_index("equipo"))
        else:
            st.warning("⚠️ No se encontró la columna 'nombre' en los datos.")

        elif modulo == "alisto_form":
        try:
            mostrar_formulario_alisto(
                GOOGLE_SHEET_ID="1o-GozoYaU_4Ra2KgX05Yi4biDV9zcd6BGdqOdSxKAv0",
                service_account_info=st.secrets["gcp_service_account"],
                nombre_empleado=st.session_state.nombre_empleado,
                codigo_empleado=st.session_state.codigo_empleado
            )
        except Exception as e:
            st.error(f"❌ Error al cargar el formulario de alisto: {e}")

    elif modulo == "alisto_panel":
        if st.session_state.rol_handheld == "admin":
            try:
                mostrar_panel_alisto(conectar_sit_hh)
            except Exception as e:
                st.error(f"❌ Error al cargar el panel de productividad: {e}")
        else:
            st.warning("⚠️ Acceso restringido: solo administradores pueden ver el panel de productividad.")
