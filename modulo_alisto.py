import streamlit as st
from datetime import datetime
import gspread
from google.oauth2.service_account import Credentials

# 🔐 Conexión segura a Google Sheets usando st.secrets
def conectar_hoja_productividad(service_account_info):
    GOOGLE_SHEET_ID = "1PtUtGidnJkZZKW5CW4IzMkZ1tFk9dJLrGKe9vMwg0N0"

    scope = [
        "https://www.googleapis.com/auth/spreadsheets",
        "https://www.googleapis.com/auth/drive"
    ]

    try:
        credentials = Credentials.from_service_account_info(service_account_info, scopes=scope)
        gc = gspread.authorize(credentials)
        libro = gc.open_by_key(GOOGLE_SHEET_ID)
        return libro.worksheet("Productividad")  # Asegúrate de que ese sea el nombre exacto
    except Exception as e:
        st.error(f"❌ Error técnico al conectar con la hoja: {e}")
        return None

# 🧮 Cálculo de eficiencia
def calcular_eficiencia(hora_inicio, hora_fin, unidades):
    try:
        t1 = datetime.combine(datetime.today(), hora_inicio)
        t2 = datetime.combine(datetime.today(), hora_fin)
        minutos = (t2 - t1).seconds / 60
        return round(unidades / minutos, 2) if minutos > 0 else 0
    except:
        return 0

# 📋 Formulario principal
def mostrar_formulario_alisto(GOOGLE_SHEET_ID, service_account_info, nombre_empleado, codigo_empleado):
    st.title("🕒 Registro de Productividad")

    placas = [
        "200", "201", "202", "203", "204", "205", "206", "207", "208", "209",
        "210", "211", "212", "213", "214", "215", "216", "216", "218",
        "300", "301", "302", "303", "304", "305", "306", "307", "308", "309",
        "310", "311", "312", "313", "314", "315", "316", "317", "318",
        "400", "401", "402", "403", "404", "405", "406", "407", "408", "409",
        "410", "411", "412", "413",
        "500", "505", "506", "507", "508", "509", "510", "511", "512", "513",
        "F01", "F02", "F03", "F04", "F05", "F06", "F07", "F08", "F09", "F10",
        "POZUELO", "SIGMA", "COMAPAN", "MAFAM", "MEGASUPER", "AUTOMERCADO",
        "DEMASA", "INOLASA", "EXPORTACION UNIMAR", "HILLTOP", "SAM", "CARTAINESA", "AUTODELI", "WALMART", "PRICSMART"
    ]

    placa = st.selectbox("🚚 Placa del vehículo", placas)
    tipo_tarea = st.selectbox("🛠️ Tipo de tarea", ["Alisto", "Despacho", "Picking", "Otro"])
    unidades = st.number_input("📦 Cantidad de líneas - Unidades", min_value=0, step=1)
    cajas = st.number_input("📦 Cantidad de líneas - Cajas", min_value=0, step=1)

    if "hora_inicio" not in st.session_state:
        st.session_state.hora_inicio = None
    if "hora_fin" not in st.session_state:
        st.session_state.hora_fin = None

    col1, col2 = st.columns(2)
    with col1:
        if st.session_state.hora_inicio is None:
            if st.button("⏱️ Registrar hora de inicio"):
                st.session_state.hora_inicio = datetime.now().time()
                st.success(f"Hora de inicio: {st.session_state.hora_inicio.strftime('%H:%M:%S')}")

    with col2:
        if st.session_state.hora_fin is None:
            if st.button("🕔 Registrar hora de fin"):
                st.session_state.hora_fin = datetime.now().time()
                st.success(f"Hora de fin: {st.session_state.hora_fin.strftime('%H:%M:%S')}")

    if st.session_state.hora_inicio and st.session_state.hora_fin:
        if st.button("💾 Guardar registro"):
            hoja = conectar_hoja_productividad(service_account_info)
            if hoja:
                fecha = datetime.now().strftime("%Y-%m-%d")
                eficiencia = calcular_eficiencia(st.session_state.hora_inicio, st.session_state.hora_fin, unidades)

                fila = [
                    fecha,
                    placa,
                    codigo_empleado,
                    nombre_empleado,
                    tipo_tarea,
                    unidades,
                    cajas,
                    st.session_state.hora_inicio.strftime("%H:%M:%S"),
                    st.session_state.hora_fin.strftime("%H:%M:%S"),
                    eficiencia
                ]

                hoja.append_row(fila)
                st.success("✅ Registro guardado correctamente.")
                st.session_state.hora_inicio = None
                st.session_state.hora_fin = None
            else:
                st.error("❌ No se pudo conectar con la hoja de productividad.")
