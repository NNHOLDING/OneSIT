import streamlit as st
from defaults import defaults

def cerrar_sesion(registrar_log):
    registrar_log(
        st.session_state.codigo_empleado,
        st.session_state.nombre_empleado,
        "Login",
        "Cierre de sesión"
    )
    for key, value in defaults.items():
        st.session_state[key] = value
    st.success("✅ Sesión cerrada correctamente")
