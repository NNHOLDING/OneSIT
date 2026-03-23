import streamlit as st
from datetime import datetime
from defaults import defaults

# 🚪 Cierre de sesión
st.markdown("---")
st.markdown("### 🚪 Cerrar sesión")

# Mostrar fecha actual sobre la imagen (esquina superior izquierda)
fecha_actual = datetime.now().strftime("%d/%m/%Y")
st.markdown(
    f"""
    <div style="position: relative; display: inline-block;">
        <div style="position: absolute; top: 10px; left: 10px; 
                    background-color: rgba(255,255,255,0.7); 
                    padding: 5px; border-radius: 5px; font-weight: bold;">
            📅 {fecha_actual}
        </div>
        <img src="ruta/a/tu/imagen.png" style="width:100%;">
    </div>
    """,
    unsafe_allow_html=True
)

if st.button("Salir", key="boton_salir"):
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

    st.success("✅ Sesión cerrada correctamente")
