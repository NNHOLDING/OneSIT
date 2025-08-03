import streamlit as st
from datetime import date, datetime
import gspread
from google.oauth2.service_account import Credentials

def mostrar_formulario_alisto(GOOGLE_SHEET_ID, service_account_info, nombre_empleado, codigo_empleado):
    st.subheader("📝 Registro de Productividad - Alisto Unimar")

    placas = [
        "200", "201", "202", "SIGMA", "WALMART", "PRICSMART"  # acortado por ejemplo
    ]

    try:
        scope = [
            "https://spreadsheets.google.com/feeds",
            "https://www.googleapis.com/auth/drive"
        ]
        credentials = Credentials.from_service_account_info(service_account_info, scopes=scope)
        gc = gspread.authorize(credentials)
        sheet = gc.open_by_key(GOOGLE_SHEET_ID).worksheet("Productividad")
    except Exception as e:
        st.error("❌ Error al conectar con la hoja Productividad.")
        return

    fecha = st.date_input("📅 Fecha de operación", value=date.today())
    placa = st.selectbox("🚚 Placa", placas)
    st.text_input("🧑‍💼 Código empleado", value=codigo_empleado, disabled=True)
    st.text_input("👤 Nombre del empleado", value=nombre_empleado, disabled=True)

    tipo_tarea = "Alisto de producto"
    st.text_input("⚙️ Tipo de tarea", value=tipo_tarea, disabled=True)

    cantidad_lineas_unidades = st.number_input("📦 Cantidad líneas - Unidades", min_value=0, step=1)
    cantidad_lineas_cajas = st.number_input("📦 Cantidad líneas - Cajas", min_value=0, step=1)

    if st.button("🕒 Marcar hora de inicio") and "alisto_hora_inicio" not in st.session_state:
        st.session_state["alisto_hora_inicio"] = datetime.now().time()

    if st.button("🕒 Marcar hora de fin") and "alisto_hora_fin" not in st.session_state:
        st.session_state["alisto_hora_fin"] = datetime.now().time()

    hora_inicio = st.session_state.get("alisto_hora_inicio", None)
    hora_fin = st.session_state.get("alisto_hora_fin", None)

    def calcular_eficiencia(u, c, inicio, fin):
        total_lineas = u + c
        if not inicio or not fin:
            return 0
        duracion = (datetime.combine(date.today(), fin) - datetime.combine(date.today(), inicio)).seconds / 3600
        return round(total_lineas / duracion, 2) if duracion > 0 else 0

    eficiencia = calcular_eficiencia(cantidad_lineas_unidades, cantidad_lineas_cajas, hora_inicio, hora_fin)
    hora_registro = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    if st.button("💾 Guardar registro"):
        try:
            id_registro = len(sheet.get_all_values()) + 1
            fila = [
                id_registro,
                hora_registro,
                str(fecha),
                codigo_empleado,
                nombre_empleado,
                placa,
                tipo_tarea,
                cantidad_lineas_unidades,
                cantidad_lineas_cajas,
                str(hora_inicio),
                str(hora_fin),
                eficiencia,
                hora_registro  # Hora fin de registro
            ]
            sheet.append_row(fila)
            st.success(f"✅ Registro #{id_registro} guardado exitosamente.")
            for key in ["alisto_hora_inicio", "alisto_hora_fin"]:
                st.session_state.pop(key, None)
            st.rerun()
        except Exception as e:
            st.error("❌ Error al guardar en Google Sheets.")
            st.error(f"Detalles: {e}")