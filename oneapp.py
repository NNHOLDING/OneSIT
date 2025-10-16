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
    if modulo == "📋 Panel Administrativo":
        if st.session_state.rol_handheld != "admin":
            st.error("⛔ No tienes permisos para acceder a este módulo.")
        else:
            # ... contenido del panel administrativo ...

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
        # ... contenido del panel de certificaciones ...

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
