elif modulo == "🌡️ Registro de Temperatura":
    st.title("🌡️ Registro de Temperatura")
    hoja = conectar_sit_hh().worksheet("TTemperatura")

    # Fecha y hora local CRC
    ahora = datetime.now(cr_timezone)
    fecha_actual = ahora.strftime("%d/%m/%Y")
    hora_actual = ahora.strftime("%H:%M")

    st.text_input("📅 Fecha", value=fecha_actual, disabled=True)
    st.text_input("⏰ Hora", value=hora_actual, disabled=True)

    # Usuario y nombre desde sesión
    codigo = st.session_state.codigo_empleado
    hoja_usuarios = conectar_sit_hh().worksheet("usuarios")
    datos_usuarios = hoja_usuarios.get_all_values()
    df_usuarios = pd.DataFrame(datos_usuarios[1:], columns=datos_usuarios[0])
    df_usuarios.columns = df_usuarios.columns.str.strip().str.lower()
    nombre = df_usuarios[df_usuarios["codigoempleado"].str.lower() == codigo.lower()]["nombreempleado"].values[0]

    st.text_input("👤 Usuario", value=codigo, disabled=True)
    st.text_input("🧑 Nombre de usuario", value=nombre, disabled=True)

    # Contenedor
    congelados = [f"Contenedor congelado {str(i).zfill(2)}" for i in range(1, 11)]
    refrigerados = [f"Contenedor refrigerado {str(i).zfill(2)}" for i in range(1, 11)]
    opciones_contenedor = congelados + refrigerados
    contenedor = st.selectbox("📦 Contenedor", opciones_contenedor)

    # Temperatura
    temperatura = st.number_input("🌡️ Temperatura (°C)", step=0.1, format="%.1f")

    # Rango definido por tipo
    if "congelado" in contenedor.lower():
        rango_definido = -18.0
    else:
        rango_definido = -0.5
    st.text_input("📏 Rango definido", value=f"{rango_definido}°C", disabled=True)

    # Valoración
    diferencia = temperatura - rango_definido
    if abs(diferencia) < 1:
        valoracion = "Normal"
    elif abs(diferencia) < 3:
        valoracion = "Moderada"
    elif abs(diferencia) < 5:
        valoracion = "Alta"
    else:
        valoracion = "Crítica"
    st.text_input("🧮 Valoración", value=valoracion, disabled=True)

    # Foto (solo referencia visual, no captura directa desde cámara en Streamlit)
    st.info("📷 Para capturar una foto, usa tu cámara y súbela aquí.")
    foto = st.file_uploader("Sube la foto", type=["jpg", "jpeg", "png"])

    # Dispositivo
    dispositivo = st.text_input("💻 Dispositivo", value=st.session_state.get("device_name", ""), disabled=True)

    # Guardar registro
    if st.button("✅ Guardar registro"):
        fila = [
            fecha_actual,
            hora_actual,
            codigo,
            nombre,
            "",  # Almacén (puedes agregarlo si lo necesitas)
            contenedor,
            temperatura,
            f"{rango_definido}°C",
            valoracion,
            "",  # Foto (se gestiona aparte)
            dispositivo
        ]
        hoja.append_row(fila)
        st.success("✅ Registro guardado correctamente")

        # Guardar foto en Drive (requiere integración con Google Drive API)
        if foto:

            st.warning("⚠️ La carga directa a Drive requiere configuración adicional con la API de Google Drive.")
