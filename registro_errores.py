import streamlit as st
import datetime
from google_sheets import conectar_sit_hh

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
    st.markdown(f"🗓️ Fecha actual: `{fecha_actual}`")

    producto = st.text_input("📦 Escanea o ingresa el código del producto")
    descripcion = st.text_input("Descripción del producto")
    pallet = st.text_input("🧺 Escanea o ingresa el código del pallet")
    tipo_error = st.selectbox("Tipo de error", ["UNIDADES", "CAJAS", "OTRO"])
    error_unidades = st.number_input("Cantidad con error (Unidades)", min_value=0)
    error_cajas = st.number_input("Cantidad con error (Cajas)", min_value=0)
    placa = st.text_input("Placa del vehículo")
    chequeador = st.text_input("Nombre del chequeador")

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
