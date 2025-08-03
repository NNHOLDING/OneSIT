import streamlit as st
from datetime import datetime
import gspread
from google.oauth2.service_account import Credentials

# 👉 Autenticación y conexión con Google Sheets
def conectar_hoja_productividad():
    GOOGLE_SHEET_ID = "1PtUtGidnJkZZKW5CW4IzMkZ1tFk9dJLrGKe9vMwg0N0"

    service_account_info = {
        "type": "service_account",
        "project_id": "tu-proyecto",
        "private_key_id": "xxxx",
        "private_key": "-----BEGIN PRIVATE KEY-----\nTU_LLAVE\n-----END PRIVATE KEY-----\n",
        "client_email": "smartoneintelligence@onesit.iam.gserviceaccount.com",
        "client_id": "xxxx",
        "auth_uri": "https://accounts.google.com/o/oauth2/auth",
        "token_uri": "https://oauth2.googleapis.com/token",
        "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
        "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/smartoneintelligence%40onesit.iam.gserviceaccount.com"
    }

    scope = [
        "https://www.googleapis.com/auth/spreadsheets",
        "https://www.googleapis.com/auth/drive"
    ]

    try:
        credentials = Credentials.from_service_account_info(service_account_info, scopes=scope)
        gc = gspread.authorize(credentials)
        libro = gc.open_by_key(GOOGLE_SHEET_ID)
        nombre_hoja = "Productividad"
        if nombre_hoja in [hoja.title for hoja in libro.worksheets()]:
            return libro.worksheet(nombre_hoja)
        else:
            hoja_nueva = libro.add_worksheet(title=nombre_hoja, rows="1000", cols="20")
            encabezados = [
                "ID", "Hora de registro", "Fecha", "Código empleado", "Nombre del empleado",
                "Placa", "Tipo de tarea", "Cantidad líneas - Unidades", "Cantidad líneas - Cajas",
                "Hora de inicio", "Hora de fin", "Eficiencia", "Hora fin de registro"
            ]
            hoja_nueva.insert_row(encabezados, index=1)
            return hoja_nueva
    except Exception as e:
        print(f"❌ Error de conexión: {e}")
        return None

# 👉 Función para calcular eficiencia
def calcular_eficiencia(hora_inicio, hora_fin, unidades):
    try:
        t1 = datetime.combine(datetime.today(), hora_inicio)
        t2 = datetime.combine(datetime.today(), hora_fin)
        minutos = (t2 - t1).seconds / 60
        return round(unidades / minutos, 2) if minutos > 0 else 0
    except:
        return 0

# 📝 Formulario Streamlit para registrar productividad
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

    # Inputs estándar
    placa = st.selectbox("🚚 Placa del vehículo", placas)
    tipo_tarea = st.selectbox("🛠️ Tipo de tarea", ["Alisto", "Despacho", "Picking", "Otro"])
    unidades = st.number_input("📦 Cantidad de líneas - Unidades", min_value=0, step=1)
    cajas = st.number_input("📦 Cantidad de líneas - Cajas", min_value=0, step=1)

    # Inicializar estados de sesión
    if "hora_inicio" not in st.session_state:
        st.session_state.hora_inicio = None
    if "hora_fin" not in st.session_state:
        st.session_state.hora_fin = None

    # Botones para registrar hora
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

    # Botón para guardar registro
    if st.session_state.hora_inicio and st.session_state.hora_fin:
        if st.button("💾 Guardar registro"):
            hoja = conectar_hoja_productividad()
            if hoja:
                ahora = datetime.now().strftime("%H:%M:%S")
                fecha = datetime.now().strftime("%Y-%m-%d")
                eficiencia = calcular_eficiencia(st.session_state.hora_inicio, st.session_state.hora_fin, unidades)
                fila = [
                    "", ahora, fecha, codigo_empleado, nombre_empleado,
                    placa, tipo_tarea, unidades, cajas,
                    st.session_state.hora_inicio.strftime("%H:%M:%S"),
                    st.session_state.hora_fin.strftime("%H:%M:%S"),
                    eficiencia, ahora
                ]
                hoja.append_row(fila)
                st.success("✅ Registro guardado correctamente.")
                # Resetear horas si deseas
                st.session_state.hora_inicio = None
                st.session_state.hora_fin = None
            else:
                st.error("❌ No se pudo conectar con la hoja de productividad.")
