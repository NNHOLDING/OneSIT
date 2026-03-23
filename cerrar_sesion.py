import streamlit as st
from defaults import defaults
from logenvios import registrar_log   # ajusta el import según dónde tengas registrar_log

def cerrar_sesion():
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

    # Opcional: mostrar confirmación
    st.success("✅ Sesión cerrada correctamente")