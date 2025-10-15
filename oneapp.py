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
        "🕒 Productividad",
        "📝 Gestión de Jornada",
        "🚨 Registro de Errores",
        "🌡️ Registro de Temperatura",
        "🧪 Prueba de Ubicación",
        "🎓 Control de Certificación",  # 👈 Nuevo módulo
        "📊 Panel de Certificaciones",  # ✅ Asegúrate de que esté aquí

    ]

    modulos_usuario = [
        "📦 Registro de Handhelds",
        "🕒 Productividad",
        "📝 Gestión de Jornada",
        "🌡️ Registro de Temperatura",
        "🧪 Prueba de Ubicación",
        "🎓 Control de Certificación",  # 👈 Nuevo módulo
    ]

    opciones_menu = modulos_admin if st.session_state.rol_handheld == "admin" else modulos_usuario
    modulo = st.sidebar.selectbox("🧩 Selecciona el módulo", opciones_menu)

    # 📦 Registro
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

    # 📅 Certificaciones por Día
            st.subheader("📅 Certificaciones por Día")
            cert_por_dia = df_filtrado.groupby(df_filtrado["fecha"].dt.date).size().reset_index(name="Certificaciones")
            st.dataframe(cert_por_dia)
            st.bar_chart(cert_por_dia.set_index("fecha"))

            # 📄 Registros del Día Actual
            st.subheader(f"📄 Registros del Día ({hoy})")
            registros_hoy = df_filtrado[df_filtrado["fecha"].dt.date == hoy]
            st.dataframe(registros_hoy)

            # 🏢 Rutas Certificadas por Empresa
            if "empresa" in df_filtrado.columns and "ruta" in df_filtrado.columns:
                st.subheader("🏢 Rutas Certificadas por Empresa")
                rutas_por_empresa = df_filtrado.groupby("empresa")["ruta"].nunique().reset_index(name="Rutas Certificadas")
                st.dataframe(rutas_por_empresa)

                st.subheader("📊 Cantidad de Rutas Certificadas por Empresa")
                st.bar_chart(rutas_por_empresa.set_index("empresa"))

            # ⏱️ Duración Promedio por Ruta
            if "ruta" in df_filtrado.columns and "duracion" in df_filtrado.columns:
                st.subheader("⏱️ Duración Promedio por Ruta")
                duracion_por_ruta = df_filtrado.groupby("ruta")["duracion"].mean().reset_index()
                duracion_por_ruta["duracion"] = duracion_por_ruta["duracion"].round(2)
                st.dataframe(duracion_por_ruta)
                st.bar_chart(duracion_por_ruta.set_index("ruta"))

            # ⏱️ Duración Promedio por Certificador
            if "certificador" in df_filtrado.columns and "duracion" in df_filtrado.columns:
                st.subheader("⏱️ Duración Promedio por Certificador")
                duracion_por_cert = df_filtrado.groupby("certificador")["duracion"].mean().reset_index()
                duracion_por_cert["duracion"] = duracion_por_cert["duracion"].round(2)
                st.dataframe(duracion_por_cert)
                st.bar_chart(duracion_por_cert.set_index("certificador"))

                # 📋 Resumen del Día por Certificador
                st.subheader(f"📋 Resumen del Día por Certificador ({hoy})")
                resumen_hoy = registros_hoy.groupby("certificador").agg({
                    "ruta": "nunique",
                    "duracion": "mean"
                }).reset_index().rename(columns={"ruta": "Rutas Certificadas", "duracion": "Duración Promedio"})
                resumen_hoy["Duración Promedio"] = resumen_hoy["Duración Promedio"].round(2)
                st.dataframe(resumen_hoy)

            # 🥧 Gráfico Pastel del Mes por Usuario
            if "usuario" in df_filtrado.columns and "ruta" in df_filtrado.columns:
                st.subheader("🥧 Rutas Certificadas por Usuario (Mes Actual)")
                mes_actual = hoy.month
                df_mes = df_filtrado[df_filtrado["fecha"].dt.month == mes_actual]
                rutas_por_usuario = df_mes.groupby("usuario")["ruta"].nunique().reset_index(name="Rutas Certificadas")
                st.dataframe(rutas_por_usuario)

                import plotly.express as px
                st.plotly_chart(px.pie(rutas_por_usuario, names="usuario", values="Rutas Certificadas", title="Distribución por Usuario"))

            # 📊 Actividad por Usuario
            st.subheader("📊 Actividad por Usuario")
            resumen = df_filtrado.groupby("nombre").size().reset_index(name="Registros")
            st.dataframe(resumen)
            st.bar_chart(resumen.set_index("nombre"))

            # 🔧 Actividad por Equipo
            if "equipo" in df_filtrado.columns:
                st.subheader("🔧 Actividad por Equipo")
                resumen_eq = df_filtrado.groupby("equipo").size().reset_index(name="Movimientos")
                st.dataframe(resumen_eq)
                st.bar_chart(resumen_eq.set_index("equipo"))

                    # 📥 Descargar CSV
        st.subheader("📥 Descargar Datos")
        csv = df_filtrado.to_csv(index=False).encode("utf-8")
        st.download_button("📥 Descargar CSV", csv, "certificaciones.csv", "text/csv")
    else:
        st.warning("⚠️ No se encontraron datos válidos en la hoja 'HH'.")


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

    # 📝 Gestión de Jornada
    elif modulo == "📝 Gestión de Jornada":
        gestionar_jornada(conectar_sit_hh, st.session_state.nombre_empleado)
        if st.session_state.rol_handheld == "admin":
            st.markdown("---")
            mostrar_jornadas(conectar_sit_hh)

          # 🚨 Registro de Errores
    elif modulo == "🚨 Registro de Errores":
        mostrar_formulario_errores

        # 🎓 Control de Certificación
    elif modulo == "🎓 Control de Certificación":
        st.title("🎓 Control de certificación de rutas Sigma Alimentos")

        fecha_actual = datetime.now(cr_timezone).strftime("%Y-%m-%d")
        st.text_input("Fecha", value=fecha_actual, disabled=True)

        ruta = st.selectbox("Ruta", ["100", "200", "300", "400", "500", "600", "700", "800", "otro"])

        def obtener_usuarios_certificacion():
            hoja = conectar_sit_hh().worksheet("usuarios")
            datos = hoja.get_all_values()
            return sorted([fila[1] for fila in datos[1:] if fila[1]])

        usuarios = obtener_usuarios_certificacion()
        certificador = st.selectbox("Certificador", usuarios)
        persona_conteo = st.selectbox("Persona conteo", usuarios)

        hora_actual_crc = datetime.now(cr_timezone).time().replace(second=0, microsecond=0)
        hora_inicio = st.time_input("Hora inicio", value=hora_actual_crc)
        hora_fin = st.time_input("Hora fin", value=hora_actual_crc)

        if st.button("📥 Guardar Certificación"):
            campos = {
                "Ruta": ruta,
                "Certificador": certificador,
                "Persona conteo": persona_conteo,
                "Hora inicio": hora_inicio,
                "Hora fin": hora_fin
            }
            faltantes = [campo for campo, valor in campos.items() if not valor]
            if faltantes:
                st.warning(f"⚠️ Debes completar los siguientes campos: {', '.join(faltantes)}")
            else:
                try:
                    formato = "%H:%M"
                    inicio_dt = datetime.strptime(hora_inicio.strftime(formato), formato)
                    fin_dt = datetime.strptime(hora_fin.strftime(formato), formato)
                    duracion = int((fin_dt - inicio_dt).total_seconds() / 60)
                    if duracion < 0:
                        st.error("⚠️ La hora de fin no puede ser anterior a la hora de inicio.")
                    else:
                        hora_registro = datetime.now(cr_timezone).strftime("%H:%M:%S")
                        site = "Site Alajuela"

                        hoja = conectar_sit_hh().worksheet("TCertificaciones")
                        hoja.append_row([
                            fecha_actual, ruta, certificador, persona_conteo,
                            hora_inicio.strftime(formato), hora_fin.strftime(formato),
                            duracion, hora_registro, site
                        ])
                        st.success("✅ Certificación registrada correctamente.")
                except Exception as e:
                    st.error(f"❌ Error al registrar certificación: {e}")

    # 🚪 Cierre de sesión
    st.markdown("---")
    st.markdown("### 🚪 Cerrar sesión")
    if st.button("Salir", key="boton_salir"):
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

   







