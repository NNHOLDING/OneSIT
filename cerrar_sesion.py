import streamlit as st
from defaults import defaults

def cerrar_sesion(registrar_log):
    # Registrar cierre de sesión en LogEnvios
    registrar_log(
        st.session_state.codigo_empleado,
        st.session_state.nombre_empleado,
        "Login",
        "Cierre de sesión"
    )

    # Reiniciar variables de sesión con los valores por defecto
    for key, value in defaults.items():
        st.session_state[key] = value

    # Mensaje de confirmación
    st.success("✅ Sesión cerrada correctamente")
