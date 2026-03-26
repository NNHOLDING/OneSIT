import streamlit as st

def cerrar_sesion():
    from defaults import defaults
    from oneapp import registrar_log  # ajusta este import si registrar_log está en otro módulo

    registrar_log(st.session_state.codigo_empleado,
                  st.session_state.nombre_empleado,
                  "Login",
                  "Cierre de sesión")

    for key in defaults.keys():
        st.session_state[key] = False

def script_inactividad(minutos=5):
    st.markdown(f"""
    <script>
    let timeout;
    function resetTimer() {{
        clearTimeout(timeout);
        timeout = setTimeout(() => {{
            window.location.href = window.location.pathname + "?expired=true";
        }}, {minutos*60000});
    }}
    window.onload = resetTimer;
    document.onmousemove = resetTimer;
    document.onkeypress = resetTimer;
    </script>
    """, unsafe_allow_html=True)
