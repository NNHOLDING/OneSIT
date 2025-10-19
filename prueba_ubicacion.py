import streamlit as st
from streamlit_js_eval import streamlit_js_eval

def mostrar_prueba_ubicacion():
    st.title("📍 Prueba de ubicación automática")

    ubicacion = streamlit_js_eval(
        js_expressions="""
        new Promise((resolve, reject) => {
            navigator.geolocation.getCurrentPosition(
                (pos) => resolve({latitude: pos.coords.latitude, longitude: pos.coords.longitude}),
                (err) => reject(err)
            );
        })
        """,
        key="ubicacion_prueba"
    )

    if ubicacion and "latitude" in ubicacion and "longitude" in ubicacion:
        st.success("✅ Ubicación detectada:")
        st.json(ubicacion)
    else:
        st.error("❌ No se pudo obtener la ubicación. Verifica los permisos del navegador y recarga la página.")

