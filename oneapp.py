import streamlit as st
import pandas as pd
from datetime import datetime
import pytz
import gspread
from oauth2client.service_account import ServiceAccountCredentials

# 🌎 Zona horaria
cr_timezone = pytz.timezone("America/Costa_Rica")

# 🔗 Conexión con Google Sheets
def conectar_sit_hh():
    scope = [
        "https://spreadsheets.google.com/feeds",
        "https://www.googleapis.com/auth/drive"
    ]
    creds = ServiceAccountCredentials.from_json_keyfile_dict(
        st.secrets["gcp_service_account"], scope)
    client = gspread.authorize(creds)
    return client.open_by_url(
        "https://docs.google.com/spreadsheets/d/1yuorNrQVGojo1oK-QoVPF0KbipJ3q92LHAeG5_vrZX8/edit")

# 🔍 Obtener nombre por código
def obtener_nombre(codigo):
    hoja = conectar_sit_hh().worksheet("Empleados")
    datos = hoja.get_all_values()
    for fila in datos:
        if fila[0] == codigo:
            return fila[1]
    return None

# 🔐 Validar credenciales
def validar_login(usuario, contraseña):
    if usuario == "Admin" and contraseña == "Administrador":
        return "admin", "Administrador"
    elif contraseña == f"numar{usuario}":
        nombre = obtener_nombre(usuario)
        if nombre:
            return "estandar", nombre
    return None, None

# 📋 Buscar fila existente
def buscar_fila(codigo, fecha):
    hoja = conectar_sit_hh().worksheet("ENTREGA")
    datos = hoja.get_all_values()
    for idx, fila in enumerate(datos[1:], start=2):
        if fila[1] == codigo and fila[0] == fecha:
            return idx, fila
    return None, None

# 📝 Registrar actividad
def registrar_handheld(codigo, nombre, equipo, tipo):
    hoja = conectar_sit_hh().worksheet("ENTREGA")
    fecha = datetime.now(cr_timezone).strftime("%Y-%m-%d")
    hora = datetime.now(cr_timezone).strftime("%H:%M:%S")
    fila_idx, fila = buscar_fila(codigo, fecha)

    if tipo == "entrega":
        if fila and fila[4]:
            st.warning("❌ Ya se registró una entrega para hoy.")
            return
        if fila:
            hoja.update_cell(fila_idx, 5, hora)
        else:
            hoja.append_row([fecha, codigo, nombre, equipo, hora, "", "Entregado"])
        st.success("✅ Entrega registrada correctamente.")
    elif tipo == "devolucion":
        if fila and fila[5]:
            st.warning("❌ Ya se registró una devolución para hoy.")
            return
        if fila:
            hoja.update_cell(fila_idx, 6, hora)
            hoja.update_cell(fila_idx, 7, "Devuelto")
        else:
            hoja.append_row([fecha, codigo, nombre, equipo, "", hora, "Devuelto"])
        st.success("✅ Devolución registrada correctamente.")

# 📊 Cargar datos a DataFrame
def cargar_handhelds():
    hoja = conectar_sit_hh().worksheet("ENTREGA")
    datos = hoja.get_all_values()
    df = pd.DataFrame(datos[1:], columns=datos[0])
    df["Fecha"] = pd.to_datetime(df["Fecha"], errors="coerce")
    return df

# 🧼 Inicializar sesión
for key in ["logueado_handheld", "rol_handheld", "nombre_empleado", "codigo_empleado"]:
    if key not in st.session_state:
        st.session_state[key] = ""

# 👋 Mensaje al salir
if st.query_params.get("salida") == "true":
    for key in ["logueado_handheld", "rol_handheld", "nombre_empleado", "codigo_empleado"]:
        st.session_state[key] = ""
    st.success("👋 ¡Hasta pronto!")

# 🔐 Pantalla de login
if not st.session_state.logueado_handheld:
    # 🖼️ Logo en la parte superior
    st.image("https://tudominio.com/logo.png", use_container_width=True)  # ← reemplazado correctamente
    
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
        else:
            st.error("Credenciales incorrectas o usuario no válido.")
# 🧭 Interfaz si está logueado
if st.session_state.logueado_handheld:
    tabs = st.tabs(["📦 Registro de Handhelds", "📋 Panel Administrativo"])

    # 📦 Registro de entregas
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

        # 🚪 Botón salir
        st.markdown("""
            <style>
                .boton-salir-container {
                    position: fixed;
                    bottom: 20px;
                    right: 20px;
                    z-index: 9999;
                }
                .boton-salir-container button {
                    background-color: #28a745;
                    color: white;
                    font-weight: bold;
                    border-radius: 8px;
                    padding: 0.6em 1.2em;
                    font-size: 16px;
                    border: none;
                    cursor: pointer;
                }
            </style>
            <div class="boton-salir-container">
                <form action="#">
                    <button onclick="window.location.href='?salida=true'; return confirm('¿Estás seguro que deseas salir?')">🚪 Salir</button>
                </form>
            </div>
        """, unsafe_allow_html=True)

    # 📋 Panel administrativo
    if st.session_state.rol_handheld == "admin":
        with tabs[1]:
            st.title("📋 Panel Administrativo")
            df = cargar_handhelds()

            usuarios = sorted(df["Nombre"].dropna().unique())
            fecha_ini = st.date_input("Desde", value=datetime.now(cr_timezone).date())
            fecha_fin = st.date_input("Hasta", value=datetime.now(cr_timezone).date())
            usuario_sel = st.selectbox("Filtrar por Usuario", ["Todos"] + usuarios)

            df_filtrado = df[
                (df["Fecha"].dt.date >= fecha_ini) &
                (df["Fecha"].dt.date <= fecha_fin)
            ]
            if usuario_sel != "Todos":
                df_filtrado = df_filtrado[df_filtrado["Nombre"] == usuario_sel]

            st.subheader("📑 Registros")
            st.dataframe(df_filtrado)
            csv = df_filtrado.to_csv(index=False).encode("utf-8")
            st.download_button("📥 Descargar CSV", csv, "handhelds.csv", "text/csv")

            st.subheader("📊 Actividad por Usuario")
            resumen = df_filtrado.groupby("Nombre").size().reset_index(name="Registros")
            st.dataframe(resumen)
            st.bar_chart(resumen.set_index("Nombre"))

            st.subheader("🔧 Actividad por Equipo")
            resumen_eq = df_filtrado.groupby("Equipo").size().reset_index(name="Movimientos")
            st.dataframe(resumen_eq)
            st.bar_chart(resumen_eq.set_index("Equipo"))

            st.markdown("""
    <style>
        .boton-salir-container {
            position: fixed;
            bottom: 20px;
            right: 20px;
            z-index: 9999;
        }
        .boton-salir-container button {
            background-color: #28a745;
            color: white;
            font-weight: bold;
            border-radius: 8px;
            padding: 0.6em 1.2em;
            font-size: 16px;
            border: none;
            cursor: pointer;
        }
    </style>
    <div class="boton-salir-container">
        <form action="#">
            <button onclick="window.location.href='?salida=true'; return confirm('¿Estás seguro que deseas salir?')">
                🚪 Salir
            </button>
        </form>
    </div>
""", unsafe_allow_html=True)




