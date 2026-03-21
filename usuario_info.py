import streamlit as st

def mostrar_usuario_info():
    if "nombre_empleado" in st.session_state and "codigo_empleado" in st.session_state:
        st.markdown(f"""
            <div style='
                background-color: #e6f2ff; 
                padding: 15px; 
                border-radius: 8px; 
                margin-bottom: 20px;
                border: 1px solid #99ccff;
            '>
                <h3 style='color:#004466;'>👤 Usuario Logeado</h3>
                <p><strong>Nombre:</strong> {st.session_state.nombre_empleado}</p>
                <p><strong>Código:</strong> {st.session_state.codigo_empleado}</p>
                <p><strong>Rol:</strong> {st.session_state.rol_handheld}</p>
            </div>
        """, unsafe_allow_html=True)