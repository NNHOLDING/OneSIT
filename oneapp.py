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
from modulo_alisto import mostrar_formulario_alisto  # 👉 módulo integrado

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

def cargar_handhelds():
    hoja = conectar_sit_hh().worksheet("HH")
    datos = hoja.get_all_values()
    if datos and len(datos[0]) > 0:
        df = pd.DataFrame(datos[1:], columns=datos[0])
        df.columns = df.columns.str.strip().str.lower()
        df["fecha"] = pd.to_datetime(df["fecha"], errors="coerce")
        return df
    else:
        st.warning("⚠️ No se pudieron cargar datos desde la hoja HH.")
        return pd.DataFrame()

# 🔐 Login
if not st.session_state.logueado_handheld:
    url_logo = "https://drive.google.com/uc?export=view&id=1YzqBlolo6MZ8JYzUJVvr7LFvTPP5WpM2"
    try:
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

# 🖼️ Logo institucional
if st.session_state.logueado_handheld and not st.session_state.confirmar_salida:
    st.markdown(
        "<div style='text-align: center;'>"
        "<img src='https://raw.githubusercontent.com/NNHOLDING/marcas_sit/main/28NN.PNG.jpg' width='250'>"
        "</div>",
        unsafe_allow_html=True
    )

# 🧭 Interfaz principal post-login
if st.session_state.logueado_handheld:
    tabs = st.tabs([
        "📦 Registro de Handhelds",
        "📋 Panel Administrativo",
        "🕒 Productividad",
        "📝 Gestión de Jornada"
    ])

    # 📦 Registro
    with tabs[0]:
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
                    equipo, "entrega")
        with col2:
            if st.button("✅ Guardar Devolución"):
                registrar_handheld(
                    st.session_state.codigo_empleado,
                    st.session_state.nombre_empleado,
                    equipo, "devolucion")

    # 📋 Panel Administrativo
    with tabs[1]:
        if st.session_state.rol_handheld == "admin":
            st.title("📋 Panel Administrativo")
            df = cargar_handhelds()

            if not df.empty and "nombre" in df.columns:
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

                csv = df_filtrado.to_csv(index=False).encode("utf-8")
                st.download_button("📥 Descargar CSV", csv, "handhelds.csv", "text/csv")

                # Actividad por Usuario
                st.subheader("📊 Actividad por Usuario")
                if "nombre" in df_filtrado.columns:
                    resumen = df_filtrado.groupby("nombre").size().reset_index(name="Registros")
                    st.dataframe(resumen)
                    st.bar_chart(resumen.set_index("nombre"))

                # Actividad por Equipo
                st.subheader("🔧 Actividad por Equipo")
                if "equipo" in df_filtrado.columns:
                    resumen_eq = df_filtrado.groupby("equipo").size().reset_index(name="Movimientos")
                    st.dataframe(resumen_eq)
                    st.bar_chart(resumen_eq.set_index("equipo"))
                else:
                    st.warning("⚠️ No se encuentra la columna 'equipo'.")

            else:
                st.warning("⚠️ No se encontró la columna 'nombre' en los datos.")

    # 🕒 Productividad
    with tabs[2]:
        # Título eliminado para evitar duplicación
        if st.session_state.rol_handheld == "admin":
            mostrar_jornadas(conectar_sit_hh)
        else:
            mostrar_formulario_alisto(
                GOOGLE_SHEET_ID="1o-GozoYaU_4Ra2KgX05Yi4biDV9zcd6BGdqOdSxKAv0",
                service_account_info=st.secrets["gcp_service_account"],
                nombre_empleado=st.session_state.nombre_empleado,
                codigo_empleado=st.session_state.codigo_empleado
            )

    # 📝 Gestión de Jornada
    with tabs[3]:
        # Título eliminado para evitar duplicación
        gestionar_jornada(conectar_sit_hh, st.session_state.nombre_empleado)

    # 🚪 Cierre de sesión
    if not st.session_state.confirmar_salida:
        st.markdown("---")
        st.markdown("### 🚪 Cerrar sesión")
        if st.button("Salir", key="boton_salir"):
            st.session_state.confirmar_salida = True

    elif st.session_state.confirmar_salida:
        st.markdown("## ¿Estás seguro que deseas cerrar sesión?")
        col1, col2 = st.columns(2)
        with col1:
            if st.button("✅ Sí, cerrar sesión", key="boton_confirmar_salir"):
                st.success("¡Hasta pronto! 👋 La sesión se ha cerrado correctamente.")
                for key in ["logueado_handheld", "rol_handheld", "nombre_empleado", "codigo_empleado", "confirmar_salida"]:
                    st.session_state[key] = False if key == "logueado_handheld" else ""
                st.rerun()
        with col2:
            if st.button("↩️ No, regresar", key="boton_cancelar_salir"):
                st.session_state.confirmar_salida = False

# 🧾 Footer institucional
st.markdown("""
    <hr style="margin-top: 50px; border: none; border-top: 1px solid #ccc;" />
    <div style="text-align: center; color: gray; font-size: 0.9em; margin-top: 20px;">
        NN HOLDING SOLUTIONS, Ever Be Better &copy; 2025, Todos los derechos reservados
    </div>
""", unsafe_allow_html=True)
