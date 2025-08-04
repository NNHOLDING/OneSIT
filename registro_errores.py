import streamlit as st
import cv2
from pyzbar.pyzbar import decode
import datetime

# -------- SCAN SIMILAR A APPSHEET (USANDO CÁMARA) --------
def escanear_codigo():
    st.info("Activando cámara... (presiona 'q' para cerrar)")

    cap = cv2.VideoCapture(0)
    codigo_detectado = None

    while True:
        ret, frame = cap.read()
        for barcode in decode(frame):
            codigo_detectado = barcode.data.decode('utf-8')
            st.success(f"Código detectado: {codigo_detectado}")
            cap.release()
            return codigo_detectado

        cv2.imshow('Escáner de código', frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()
    return None

# -------- FORMULARIO PRINCIPAL --------
def mostrar_formulario():
    st.title("📋 TRegistro - Registro de Errores")

    fecha_actual = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    st.write(f"🗓️ Fecha: {fecha_actual}")

    st.subheader("📦 Producto")
    if st.button("Escanear código de producto"):
        producto = escanear_codigo()
    else:
        producto = st.text_input("Código manual")

    st.subheader("🧺 Pallet")
    if st.button("Escanear código de pallet"):
        pallet = escanear_codigo()
    else:
        pallet = st.text_input("Código pallet manual")

    tipo_error = st.selectbox("Tipo de error", ["UNIDADES", "CAJAS", "OTRO"])
    error_unidades = st.number_input("Cantidad con error (Unidades)", min_value=0)
    error_cajas = st.number_input("Cantidad con error (Cajas)", min_value=0)
    placa = st.text_input("Placa asociada")
    usuario = st.text_input("Usuario")
    nombre = st.text_input("Nombre")
    chequeador = st.text_input("Chequeador")

    if st.button("✅ Registrar"):
        st.success("Datos registrados correctamente (puedes conectar gspread aquí).")

# -------- EJECUCIÓN --------
if __name__ == "__main__":
    mostrar_formulario()