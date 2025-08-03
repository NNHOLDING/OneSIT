import streamlit as st
from datetime import date, datetime
import gspread
from google.oauth2.service_account import Credentials

def mostrar_formulario_alisto(GOOGLE_SHEET_ID, service_account_info, nombre_empleado, codigo_empleado):
    st.subheader("📝 Registro de Productividad - Alisto Unimar")

    placas = [
        "200", "201", "202", "SIGMA", "WALMART", "PRICSMART"
    ]
    tipo_tarea = "Alisto de producto"

    try:
        # 🔑 Autenticación
        scope = [
            "https://spreadsheets.google.com/feeds",
            "https://www.googleapis.com/auth/drive"
        ]
        credentials = Credentials.from_service_account_info(service_account_info, scopes=scope)
        gc = gspread.authorize(credentials)

        # 📖 Abrir el libro
        libro = gc.open_by_key(GOOGLE_SHEET_ID)
        hojas = libro.worksheets()
        nombres_hojas = [hoja.title for hoja in hojas]

        # 📄 Buscar o crear hoja Productividad
        if "Productividad" in nombres_hojas:
            sheet = libro.worksheet("Productividad")
        else:
            st.warning("⚠️ La hoja 'Productividad' no existe. Se está creando...")
            sheet = libro.add_worksheet(title="Productividad", rows="1000", cols="20")
            encabezados = [
                "ID", "Hora de registro", "Fecha", "Código empleado", "Nombre del empleado",
                "Placa", "Tipo de tarea", "Cantidad líneas - Unidades", "Cantidad líneas - Cajas",
                "Hora de inicio", "Hora de fin", "Eficiencia", "Hora fin de registro"
            ]
            sheet.insert_row(encabezados, index=1)
            st.success("✅ Hoja 'Productividad' creada correctamente.")

    except Exception as e:
        st.error("❌ Error al conectar o preparar la hoja Productividad.")
        st.error(f"📛 Detalles técnicos: {type(e).__name__} — {e}")
        return

    # 📝 Formulario
    fecha = st.date_input("📅 Fecha", value=date.today())
    placa = st.selectbox("🚚 Placa", placas)
    st.text_input("🧑‍💼 Código empleado", value=codigo_empleado, disabled=True)
    st.text_input("👤 Nombre del empleado", value=nombre_empleado, disabled=True)
    st.text_input("⚙️ Tipo de tarea", value=tipo_tarea, disabled=True)

    unidades = st.number_input("📦 Cantidad líneas - Unidades", min_value=0, step=1)
    cajas = st.number_input("📦 Cantidad líneas - Cajas", min_value=0, step=1)

    if st.button("🕒 Marcar hora de inicio") and "alisto_hora_inicio" not in st.session_state:
        st.session_state["alisto_hora_inicio"] = datetime.now().time()

    if st.button("🕒 Marcar hora de fin") and "alisto_hora_fin" not in st.session_state:
        st.session_state["alisto_hora_fin"] = datetime.now().time()

    hora_inicio = st.session_state.get("alisto_hora_inicio")
    hora_fin = st.session_state.get("alisto_hora_fin")

    def calcular_eficiencia(u, c, inicio, fin):
        total = u + c
        if not inicio or not fin:
            return 0
        duracion_horas = (datetime.combine(date.today(), fin) - datetime.combine(date.today(), inicio)).seconds / 3600
        return round(total / duracion_horas, 2) if duracion_horas > 0 else 0

    eficiencia = calcular_eficiencia(unidades, cajas, hora_inicio, hora_fin)
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
                int(unidades),
                int(cajas),
                str(hora_inicio),
                str(hora_fin),
                eficiencia,
                hora_registro
            ]
            sheet.append_row(fila)
            st.success(f"✅ Registro #{id_registro} guardado correctamente.")
            for key in ["alisto_hora_inicio", "alisto_hora_fin"]:
                st.session_state.pop(key, None)
            st.rerun()
        except Exception as e:
            st.error("❌ Error al guardar el registro.")
            st.error(f"📛 Detalles técnicos: {type(e).__name__} — {e}")
