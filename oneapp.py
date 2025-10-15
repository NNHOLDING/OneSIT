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
        "🧪 Prueba de Ubicación"
        "🎓 Control de Certificación"  # 👈 Nuevo módulo

    ]

    modulos_usuario = [
        "📦 Registro de Handhelds",
        "🕒 Productividad",
        "📝 Gestión de Jornada",
        "🌡️ Registro de Temperatura",
        "🧪 Prueba de Ubicación"
        "🎓 Control de Certificación"  # 👈 Nuevo módulo
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
                    (df["fecha"].dt.date == hoy) & (df["estatus"].str.lower() == "entregado")
                ]
                devueltos_hoy = df[
                    (df["fecha"].dt.date == hoy) & (df["estatus"].str.lower() == "devuelto")
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

# 📊 Panel de Certificaciones
elif modulo == "📊 Panel de Certificaciones":
    st.title("📊 Panel de Certificaciones")
    hoja = conectar_sit_hh().worksheet("TCertificaciones")
    datos = hoja.get_all_values()

    if datos and len(datos) > 1:
        df = pd.DataFrame(datos[1:], columns=datos[0])
        df.columns = df.columns.str.strip().str.lower()
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

        hoy = datetime.now(cr_timezone).date()
        mes_actual = hoy.month

        st.subheader("📄 Registros Filtrados")
        st.dataframe(df_filtrado)

        st.subheader("📅 Certificaciones por Día")
        cert_por_dia = df_filtrado.groupby(df_filtrado["fecha"].dt.date).size().reset_index(name="Certificaciones")
        st.dataframe(cert_por_dia)
        st.bar_chart(cert_por_dia.set_index("fecha"))

        st.subheader(f"📄 Registros del Día ({hoy})")
        registros_hoy = df_filtrado[df_filtrado["fecha"].dt.date == hoy]
        st.dataframe(registros_hoy)

        st.subheader("🏢 Rutas Certificadas por Empresa")
        rutas_por_empresa = df_filtrado.groupby("empresa")["ruta"].nunique().reset_index(name="Rutas Certificadas")
        st.dataframe(rutas_por_empresa)

        st.subheader("⏱️ Duración Promedio por Ruta")
        duracion_por_ruta = df_filtrado.groupby("ruta")["duracion"].mean().reset_index()
        duracion_por_ruta["duracion"] = duracion_por_ruta["duracion"].round(2)
        st.dataframe(duracion_por_ruta)
        st.bar_chart(duracion_por_ruta.set_index("ruta"))

        st.subheader("⏱️ Duración Promedio por Certificador")
        duracion_por_cert = df_filtrado.groupby("certificador")["duracion"].mean().reset_index()
        duracion_por_cert["duracion"] = duracion_por_cert["duracion"].round(2)
        st.dataframe(duracion_por_cert)
        st.bar_chart(duracion_por_cert.set_index("certificador"))

        st.subheader(f"📋 Resumen del Día por Certificador ({hoy})")
        resumen_hoy = registros_hoy.groupby("certificador").agg({
            "ruta": "nunique",
            "duracion": "mean"
        }).reset_index().rename(columns={"ruta": "Rutas Certificadas", "duracion": "Duración Promedio"})
        resumen_hoy["Duración Promedio"] = resumen_hoy["Duración Promedio"].round(2)
        st.dataframe(resumen_hoy)

        st.subheader("🥧 Rutas Certificadas por Usuario (Mes Actual)")
        df_mes = df_filtrado[df_filtrado["fecha"].dt.month == mes_actual]
        rutas_por_usuario = df_mes.groupby("usuario")["ruta"].nunique().reset_index(name="Rutas Certificadas")
        st.dataframe(rutas_por_usuario)

        import plotly.express as px
        st.plotly_chart(px.pie(rutas_por_usuario, names="usuario", values="Rutas Certificadas", title="Distribución por Usuario"))

        st.subheader("📊 Cantidad de Rutas Certificadas por Empresa")
        rutas_empresa = df_filtrado.groupby("empresa")["ruta"].nunique().reset_index(name="Rutas Certificadas")
        st.dataframe(rutas_empresa)
        st.bar_chart(rutas_empresa.set_index("empresa"))

        st.subheader("📥 Descargar Datos")
        csv = df_filtrado.to_csv(index=False).encode("utf-8")
        st.download_button("📥 Descargar CSV", csv, "certificaciones.csv", "text/csv")
    else:
        st.warning("⚠️ No se encontraron registros en la hoja 'TCertificaciones'.")
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
        # 🚪 Cierre de sesión
    st.markdown("---")
    st.markdown("### 🚪 Cerrar sesión")
    if st.button("Salir", key="boton_salir"):
        for key in defaults.keys():
            st.session_state[key] = False if key == "logueado_handheld" else ""
        st.rerun()
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

    hora_inicio = st.time_input("Hora inicio", value=None)
    hora_fin = st.time_input("Hora fin", value=None)

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

                    hoja = conectar_sit_hh().parent.open_by_url(
                        "https://docs.google.com/spreadsheets/d/1PtUtGidnJkZZKW5CW4IzMkZ1tFk9dJLrGKe9vMwg0N0/edit"
                    ).worksheet("TCertificaciones")

                    hoja.append_row([
                        fecha_actual, ruta, certificador, persona_conteo,
                        hora_inicio.strftime(formato), hora_fin.strftime(formato),
                        duracion, hora_registro, site
                    ])
                    st.success("✅ Certificación registrada correctamente.")
            except Exception as e:
                st.error(f"❌ Error al registrar certificación: {e}")

# 🧾 Footer institucional
st.markdown("""
    <hr style="margin-top: 50px; border: none; border-top: 1px solid #ccc;" />
    <div style="text-align: center; color: gray; font-size: 0.9em; margin-top: 20px;">
        NN HOLDING SOLUTIONS, Ever Be Better &copy; 2025, Todos los derechos reservados
    </div>
""", unsafe_allow_html=True)





