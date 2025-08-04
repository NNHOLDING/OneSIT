import streamlit as st
import datetime
import pytz
from google_sheets import conectar_sit_hh

# 🌎 Zona horaria Costa Rica
cr_timezone = pytz.timezone("America/Costa_Rica")

# 🚚 Lista de placas disponibles
placas = [
    "200", "201", "202", "203", "204", "205", "206", "207", "208", "209",
    "210", "211", "212", "213", "214", "215", "216", "218",
    "300", "301", "302", "303", "304", "305", "306", "307", "308", "309",
    "310", "311", "312", "313", "314", "315", "316", "317", "318",
    "400", "401", "402", "403", "404", "405", "406", "407", "408", "409",
    "410", "411", "412", "413",
    "500", "505", "506", "507", "508", "509", "510", "511", "512", "513",
    "F01", "F02", "F03", "F04", "F05", "F06", "F07", "F08", "F09", "F10",
    "POZUELO", "SIGMA", "COMAPAN", "MAFAM", "MEGASUPER", "AUTOMERCADO",
    "DEMASA", "INOLASA", "EXPORTACION UNIMAR", "HILLTOP", "SAM",
    "CARTAINESA", "AUTODELI", "WALMART", "PRICSMART"
]

# 🧠 Función para obtener usuarios (solo si se necesita)
def obtener_usuarios():
    try:
        hoja = conectar_sit_hh().worksheet("usuarios")
        datos = hoja.get_all_values()
        return {fila[0]: fila[1] for fila in datos[1:] if len(fila) >= 2}
    except Exception as e:
        st.warning(f"⚠️ No se pudo cargar la hoja de usuarios: {e}")
        return {}

# 🔍 Función para obtener descripción desde TProductos (solo si hay código)
def obtener_descripcion_producto(codigo_producto):
    if not codigo_producto:
        return ""
    try:
        hoja = conectar_sit_hh().worksheet("TProductos")
        datos = hoja.get_all_values()
        productos = {fila[0]: fila[1] for fila in datos[1:] if len(fila) >= 2}
        return productos.get(codigo_producto, "")
    except Exception as e:
        st.warning(f"⚠️ No se pudo acceder a la hoja TProductos: {e}")
        return ""

# 📤 Enviar registro a la hoja TRegistro
def registrar_error_en_hoja(datos):
    try:
        hoja = conectar_sit_hh().worksheet("TRegistro")
        hoja.append_row([
            datos["FECHA"], datos["PLACA"], datos["PRODUCTO"], datos["DESCRIPCION DEL PRODUCTO"],
            datos["TIPO DE ERROR"], datos["ERROR UNIDADES"], datos["ERROR CAJAS"],
            datos["USUARIO"], datos["NOMBRE"], datos["CHEQUEADOR"], datos["PALLET"],
            datos["HORA"]  # Nuevo campo añadido
        ])
        return True
    except Exception as e:
        st.error(f"❌ Error al guardar en hoja TRegistro: {e}")
        return False

# 🧾 Formulario principal
def mostrar_formulario_errores():
    st.title("🚨 Registro de Errores")

    ahora = datetime.datetime.now(cr_timezone)
    fecha_actual = ahora.strftime("%d/%m/%Y")  # 💡 formato cambiado
    hora_actual = ahora.strftime("%H:%M:%S")   # ⏱️ hora separada

    st.markdown(f"🗓️ Fecha actual (CR): `{ahora.strftime('%Y-%m-%d %H:%M:%S')}`")

    # 📦 Código de producto
    producto = st.text_input("📦 Código de producto (escaneado o escrito)")

    descripcion = ""
    if producto:
        descripcion = obtener_descripcion_producto(producto)
        if not descripcion:
            st.warning("⚠️ El código de producto no se encuentra en la hoja TProductos.")
    
    st.text_input("📝 Descripción del producto", value=descripcion, disabled=True)
    pallet = st.text_input("🧺 Código del pallet (escaneado o escrito)")

    tipo_error = st.selectbox("⚠️ Tipo de error", [
        "Producto de menos",
        "Producto invertido",
        "Producto dañado",
        "Producto Vencido"
    ])

    error_unidades = st.number_input("Cantidad con error (Unidades)", min_value=0)
    error_cajas = st.number_input("Cantidad con error (Cajas)", min_value=0)
    placa = st.selectbox("🚚 Placa del vehículo", placas)

    # 👤 Usuario
    usuarios = obtener_usuarios()
    codigos = list(usuarios.keys())
    cod_usuario = st.selectbox("👤 Usuario (código)", codigos)
    nombre_usuario = usuarios.get(cod_usuario, "Desconocido")
    chequeador = st.text_input("👀 Chequeador", value=nombre_usuario, disabled=True)

    if st.button("✅ Registrar Datos"):
        datos = {
            "FECHA": fecha_actual,
            "PLACA": placa,
            "PRODUCTO": producto,
            "DESCRIPCION DEL PRODUCTO": descripcion,
            "TIPO DE ERROR": tipo_error,
            "ERROR UNIDADES": error_unidades,
            "ERROR CAJAS": error_cajas,
            "USUARIO": cod_usuario,
            "NOMBRE": nombre_usuario,
            "CHEQUEADOR": nombre_usuario,
            "PALLET": pallet,
            "HORA": hora_actual  # 🆕 campo añadido al final
        }

        exito = registrar_error_en_hoja(datos)
        if exito:
            st.success("🎉 Registro guardado correctamente en BD TRegistro.")
        else:
            st.error("❌ No se pudo guardar el registro.")

# ▶️ Ejecutar formulario
mostrar_formulario_errores()
