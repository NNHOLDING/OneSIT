# 🚪 Cierre de sesión
st.markdown("---")
st.markdown("### 🚪 Cerrar sesión")

if st.button("Salir", key="boton_salir"):
    # Registrar cierre de sesión en LogEnvios
    registrar_log(
        st.session_state.codigo_empleado,
        st.session_state.nombre_empleado,
        "Login",
        "Cierre de sesión"
    )

    # Reiniciar variables de sesión con los valores por defecto
    from defaults import defaults
    for key, value in defaults.items():
        st.session_state[key] = value

    st.success("✅ Sesión cerrada correctamente")
