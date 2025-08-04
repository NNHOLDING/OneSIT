import streamlit as st
import cv2
from pyzbar.pyzbar import decode
import datetime
from google_sheets import conectar_sit_hh

# 🎥 Función para escanear códigos por cámara
def escanear_codigo():
    st.info("Activando cámara... Presiona 'q' para cerrar.")
    cap = cv2.VideoCapture(0)
    codigo_detectado = None

    while True:
        ret, frame = cap.read()
        if not ret:
            break
        for barcode in decode(frame):
            codigo_detectado = barcode.data.decode('utf-8')
            cap.release()
            cv2.destroyAllWindows()
            return codigo_detectado

        cv2.imshow('Escáner de código', frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()
    return None

# 📤 Envía los datos a la hoja Google Sheets
def registrar_error_en_hoja(datos):
    try:
        hoja = conectar_sit_hh().worksheet("TRegistro")
        hoja.append_row([
            datos["FECHA"], datos["PLACA"], datos["PRODUCTO"], datos["DESCRIPCION DEL PRODUCTO"],
            datos["TIPO DE ERROR"], datos["ERROR UNIDADES"], datos["ERROR CAJAS"],
            datos["USUARIO"], datos["NOMBRE"], datos["CHEQUEADOR"], datos["PALLET"]
        ])
        return True
    except Exception as e:
        st.error(f"⚠️ Error al registrar: {e}")
        return False

# 🧾 Formulario completo para registrar errores
def mostrar_formulario_errores():
    st.title("🚨 Registro de Errores - TRegistro")
    fecha_actual = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    st.markdown(f"🗓️ Fecha: `{fecha_actual}`")

    st.subheader("📦 Producto")
    producto = ""
    if st.button("🔍 Escanear código de producto"):
        producto = escanear_codigo()
    producto = st.text_input("Código del producto", value=producto)

    descripcion = st.text_input("Descripción del producto")

    st.subheader("🧺 Pallet")
    pallet = ""
    if st.button("🔍 Escanear código del pallet"):
        pallet = escanear_codigo()
    pallet = st.text_input("Código del pallet", value=pallet)

    tipo_error = st.selectbox("Tipo de error", ["UNIDADES", "CAJAS", "OTRO"])
    error_unidades = st.number_input("Cantidad con error (Unidades)", min_value=0)
    error_cajas = st.number_input("Cantidad con error (Cajas)", min_value=0)
    placa = st.text_input("Placa del vehículo")
    chequeador = st.text_input("Nombre del chequeador")

    # Sesión del usuario activo (revisar si están definidos)
    usuario = st.session_state.get("codigo_empleado", "")
    nombre = st.session_state.get("nombre_empleado", "")

    if st.button("✅ Registrar"):
        datos = {
            "FECHA": fecha_actual,
            "PLACA": placa,
            "PRODUCTO": producto,
            "DESCRIPCION DEL PRODUCTO": descripcion,
            "TIPO DE ERROR": tipo_error,
            "ERROR UNIDADES": error_unidades,
            "ERROR CAJAS": error_cajas,
            "USUARIO": usuario,
            "NOMBRE": nombre,
            "CHEQUEADOR": chequeador,
            "PALLET": pallet
        }

        exito = registrar_error_en_hoja(datos)
        if exito:
            st.success("🎉 Registro guardado correctamente en la hoja TRegistro.")
        else:
            st.error("❌ No se pudo guardar el registro.")

# Prueba directa (si se ejecuta el módulo solo)
if __name__ == "__main__":
    mostrar_formulario_errores()
