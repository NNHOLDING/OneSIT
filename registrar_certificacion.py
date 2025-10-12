# 📝 Registro completo en hoja TCertificaciones
def registrar_certificacion_completa(ruta, certificador, persona_conteo, hora_inicio, hora_fin):
    try:
        # Validaciones de campos obligatorios
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
            return

        # Validación y cálculo de duración
        formato = "%H:%M"
        try:
            inicio_dt = datetime.strptime(hora_inicio, formato)
            fin_dt = datetime.strptime(hora_fin, formato)
        except ValueError:
            st.error("⚠️ Formato de hora inválido. Usa HH:MM.")
            return

        duracion = int((fin_dt - inicio_dt).total_seconds() / 60)
        if duracion < 0:
            st.error("⚠️ La hora de fin no puede ser anterior a la hora de inicio.")
            return

        # Datos automáticos
        fecha = datetime.now(cr_timezone).strftime("%Y-%m-%d")
        hora_registro = datetime.now(cr_timezone).strftime("%H:%M:%S")
        site = "Site Alajuela"

        # Conexión directa e inserción
        scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
        creds = ServiceAccountCredentials.from_json_keyfile_dict(st.secrets["gcp_service_account"], scope)
        client = gspread.authorize(creds)
        hoja = client.open_by_url("https://docs.google.com/spreadsheets/d/1PtUtGidnJkZZKW5CW4IzMkZ1tFk9dJLrGKe9vMwg0N0/edit").worksheet("TCertificaciones")

        hoja.append_row([
            fecha, ruta, certificador, persona_conteo,
            hora_inicio, hora_fin, duracion,
            hora_registro, site
        ])
        st.success("✅ Certificación registrada correctamente.")
    except Exception as e:
        st.error(f"❌ Error al registrar certificación: {e}")