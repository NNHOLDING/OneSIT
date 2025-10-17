import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt  # 👈 Aquí va
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
from modulo_temperatura import mostrar_formulario_temperatura

st.set_page_config(
    page_title="Smart Intelligence Tools",
    page_icon="https://github.com/NNHOLDING/marcas_sit/raw/main/sitfavicon.ico",
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
    st.markdown("""
        <div style='text-align: center;'>
        <img src="https://drive.google.com/uc?export=view&id=1P6OSXZMR4DI_cEgwjk1ZVJ6B8aLS1_qq" width="250">
        </div>
    """, unsafe_allow_html=True)

    # 🧩 Menú dinámico según rol
    modulos_admin = [
        "📦 Registro de Handhelds",
        "📋 Panel Administrativo",
        "📊 Panel de Certificaciones",
        "🕒 Productividad",
        "📝 Gestión de Jornada",
        "🚨 Registro de Errores",
        "🌡️ Registro de Temperatura",
        "🧪 Prueba de Ubicación"
    ]

    modulos_usuario = [
        "📦 Registro de Handhelds",
        "🕒 Productividad",
        "📝 Gestión de Jornada",
        "🌡️ Registro de Temperatura",
        "🧪 Prueba de Ubicación"
    ]

    opciones_menu = modulos_admin if st.session_state.rol_handheld == "admin" else modulos_usuario
    modulo = st.sidebar.selectbox("🧩 Selecciona el módulo", opciones_menu)

    # 📦 Registro de Handhelds
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
# 📋 Panel Administrativo
    elif modulo == "📋 Panel Administrativo":
        if st.session_state.rol_handheld != "admin":
            st.error("⛔ No tienes permisos para acceder a este módulo.")
        else:
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
# 🕒 Productividad
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

    # 📊 Panel de Certificaciones
    elif modulo == "📊 Panel de Certificaciones":
        st.title("📊 Panel de Certificaciones")
        hoja = conectar_sit_hh().worksheet("TCertificaciones")
        datos = hoja.get_all_values()

        if datos and len(datos) > 1:
            df = pd.DataFrame(datos[1:], columns=datos[0])
            df.columns = df.columns.str.strip().str.lower()

            if "fecha" not in df.columns or "certificador" not in df.columns or "ruta" not in df.columns:
                st.warning("⚠️ Las columnas necesarias no se encuentran en los datos.")
            else:
                df["fecha"] = pd.to_datetime(df["fecha"], errors="coerce")
                df["duracion"] = pd.to_numeric(df["duracion"], errors="coerce")

                rutas = sorted(df["ruta"].dropna().unique())
                certificadores = sorted(df["certificador"].dropna().unique())

                col1, col2 = st.columns(2)
                with col1:
                    fecha_ini = st.date_input("Desde", value=datetime.now(cr_timezone).date())
                with col2:
                    fecha_fin = st.date_input("Hasta", value=datetime.now(cr_timezone).date())

                ruta_sel = st.selectbox("Filtrar por Ruta", ["Todas"] + rutas)
                cert_sel = st.selectbox("Filtrar por Certificador", ["Todos"] + certificadores)

                df_filtrado = df[
                    (df["fecha"].dt.date >= fecha_ini) &
                    (df["fecha"].dt.date <= fecha_fin)
                ]
                if ruta_sel != "Todas":
                    df_filtrado = df_filtrado[df_filtrado["ruta"] == ruta_sel]
                if cert_sel != "Todos":
                    df_filtrado = df_filtrado[df_filtrado["certificador"] == cert_sel]

                st.subheader("📄 Registros Filtrados")
                st.dataframe(df_filtrado)

                # 📅 Certificaciones en los últimos 7 días
                ultima_semana = datetime.now(cr_timezone).date() - pd.Timedelta(days=7)
                df_ultimos_7 = df[df["fecha"].dt.date >= ultima_semana]

                # Agrupar por fecha en formato texto para evitar escala temporal continua
                df_ultimos_7["fecha_str"] = df_ultimos_7["fecha"].dt.strftime("%Y-%m-%d")
                rutas_por_dia = df_ultimos_7.groupby("fecha_str").size().reset_index(name="Certificaciones")

                st.subheader("📅 Certificaciones en los últimos 7 días")
                st.bar_chart(rutas_por_dia.set_index("fecha_str"))

                 # 🧑‍💼 Certificaciones por Usuario
				st.subheader("🧑‍💼 Certificaciones por Usuario")
				cert_por_usuario = df_filtrado["certificador"].value_counts()
				st.pyplot(cert_por_usuario.plot.pie(autopct="%1.1f%%", figsize=(6, 6)).figure)
				
				# 🏢 Certificaciones por Empresa
				if "empresa" in df_filtrado.columns:
				    st.subheader("🏢 Certificaciones por Empresa")
				
				    # Contar certificaciones por empresa
				    cert_por_empresa = df_filtrado["empresa"].value_counts().reset_index()
				    cert_por_empresa.columns = ["Empresa", "Certificaciones"]
				
				    # Mostrar gráfico de barras
				    st.bar_chart(cert_por_empresa.set_index("Empresa"))
				else:
				    st.info("ℹ️ No se encontró la columna 'empresa' para mostrar certificaciones por empresa.")
				
				# 🛣️ Certificaciones por Tipo de Ruta
				if "tipo_ruta" in df_filtrado.columns:
				    st.subheader("🛣️ Certificaciones por Tipo de Ruta")
				    resumen_tipo = df_filtrado["tipo_ruta"].value_counts().reset_index()
				    resumen_tipo.columns = ["Tipo de Ruta", "Certificaciones"]
				    st.bar_chart(resumen_tipo.set_index("Tipo de Ruta"))
				else:
				    st.info("ℹ️ No se encontró la columna 'tipo_ruta' para mostrar certificaciones por tipo.")
				                # 📥 Descargar CSV
				                csv = df_filtrado.to_csv(index=False).encode("utf-8")
				                st.download_button("📥 Descargar CSV", csv, "certificaciones.csv", "text/csv")

                # 📈 Duración promedio por certificador
                st.subheader("📈 Duración promedio por certificador")
                resumen_cert = df_filtrado.groupby("certificador")["duracion"].mean().reset_index()
                resumen_cert["duracion"] = resumen_cert["duracion"].round(2)
                st.dataframe(resumen_cert)
                st.bar_chart(resumen_cert.set_index("certificador"))

                # 📊 Total de certificaciones por ruta
                st.subheader("📊 Total de certificaciones por ruta")
                resumen_ruta = df_filtrado.groupby("ruta").size().reset_index(name="Certificaciones")
                st.dataframe(resumen_ruta)
                st.bar_chart(resumen_ruta.set_index("ruta"))
        else:
            st.warning("⚠️ No se encontraron registros en la hoja 'TCertificaciones'.")

    # 📝 Gestión de Jornada
    elif modulo == "📝 Gestión de Jornada":
        gestionar_jornada(conectar_sit_hh, st.session_state.nombre_empleado)
        if st.session_state.rol_handheld == "admin":
            st.markdown("---")
            mostrar_jornadas(conectar_sit_hh)

    # 🚨 Registro de Errores
    elif modulo == "🚨 Registro de Errores":
        mostrar_formulario_errores()   
# 🚪 Cierre de sesión
    st.markdown("---")
    st.markdown("### 🚪 Cerrar sesión")
    if st.button("Salir", key="boton_salir"):
        for key in defaults.keys():
            st.session_state[key] = False if key == "logueado_handheld" else ""
        st.rerun()

# 🧾 Footer institucional (fuera del login)
st.markdown("""
    <hr style="margin-top: 50px; border: none; border-top: 1px solid #ccc;" />
    <div style="text-align: center; color: gray; font-size: 0.9em; margin-top: 20px;">
        NN HOLDING SOLUTIONS, Ever Be Better &copy; 2025, Todos los derechos reservados
    </div>
""", unsafe_allow_html=True)
