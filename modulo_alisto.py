import streamlit as st
from datetime import datetime, time

def mostrar_formulario_alisto(GOOGLE_SHEET_ID, service_account_info, nombre_empleado, codigo_empleado):
    st.title("🕒 Registro de Productividad")

    placa = st.text_input("Placa del vehículo")
    tipo_tarea = st.selectbox("Tipo de tarea", ["Alisto", "Despacho", "Picking", "Otro"])
    unidades = st.number_input("Cantidad de líneas - Unidades", min_value=0, step=1)
    cajas = st.number_input("Cantidad de líneas - Cajas", min_value=0, step=1)
    hora_inicio = st.time_input("Hora de inicio", value=time(8, 0))
    hora_fin = st.time_input("Hora de fin", value=time(9, 0))

    if st.button("Guardar registro"):
        hoja = conectar_hoja_productividad()
        if hoja:
            ahora = datetime.now().strftime("%H:%M:%S")
            fecha = datetime.now().strftime("%Y-%m-%d")
            eficiencia = calcular_eficiencia(hora_inicio, hora_fin, unidades)

            fila = [
                "", ahora, fecha, codigo_empleado, nombre_empleado,
                placa, tipo_tarea, unidades, cajas,
                hora_inicio.strftime("%H:%M:%S"), hora_fin.strftime("%H:%M:%S"),
                eficiencia, ahora
            ]
            hoja.append_row(fila)
            st.success("✅ Registro guardado correctamente.")
        else:
            st.error("❌ No se pudo conectar con la hoja de productividad.")

def calcular_eficiencia(hora_inicio, hora_fin, unidades):
    try:
        t1 = datetime.combine(datetime.today(), hora_inicio)
        t2 = datetime.combine(datetime.today(), hora_fin)
        minutos = (t2 - t1).seconds / 60
        return round(unidades / minutos, 2) if minutos > 0 else 0
    except:
        return 0
