import streamlit as st
from streamlit_js_eval import streamlit_js_eval

st.title("📍 Prueba de ubicación automática")

ubicacion = streamlit_js_eval(
    js_expressions="navigator.geolocation.getCurrentPosition((pos) => ({latitude: pos.coords.latitude, longitude: pos.coords.longitude}))",
    key="ubicacion_prueba"
)

if ubicacion:
    st.write("✅ Ubicación detectada:")
    st.json(ubicacion)
else:
    st.error("❌ No se pudo obtener la ubicación. Verifica los permisos del navegador.")
