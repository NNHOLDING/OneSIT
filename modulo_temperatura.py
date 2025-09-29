from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseUpload
import io

def subir_imagen_a_drive(foto, nombre_archivo, carpeta_id, service_account_info):
    creds = service_account.Credentials.from_service_account_info(service_account_info)
    service = build('drive', 'v3', credentials=creds)

    file_metadata = {
        'name': nombre_archivo,
        'parents': [carpeta_id]
    }

    media = MediaIoBaseUpload(io.BytesIO(foto.read()), mimetype=foto.type)
    file = service.files().create(body=file_metadata, media_body=media, fields='id,webViewLink').execute()
    return file.get('webViewLink')

def mostrar_formulario_temperatura(conectar_sit_hh, cr_timezone):
    import streamlit as st
    import pandas as pd
    from datetime import datetime

    hoja = conectar_sit_hh().worksheet("TTemperatura")
    ahora = datetime.now(cr_timezone)
    fecha_actual = ahora.strftime("%d/%m/%Y")
    hora_actual = ahora.strftime("%H:%M")

    st.text_input("📅 Fecha", value=fecha_actual, disabled=True)
    st.text_input("⏰ Hora", value=hora_actual, disabled=True)

    codigo = st.session_state.codigo_empleado
    hoja_usuarios = conectar_sit_hh().worksheet("usuarios")
    datos_usuarios = hoja_usuarios.get_all_values()
    df_usuarios = pd.DataFrame(datos_usuarios[1:], columns=datos_usuarios[0])
    df_usuarios.columns = df_usuarios.columns.str.strip().str.lower()
    nombre = df_usuarios[df_usuarios["codigoempleado"].str.lower() == codigo.lower()]["nombreempleado"].values[0]

    st.text_input("👤 Usuario", value=codigo, disabled=True)
    st.text_input("🧑 Nombre de usuario", value=nombre, disabled=True)

    congelados = [f"Contenedor congelado {str(i).zfill(2)}" for i in range(1, 11)]
    refrigerados = [f"Contenedor refrigerado {str(i).zfill(2)}" for i in range(1, 11)]
    opciones_contenedor = congelados + refrigerados
    contenedor = st.selectbox("📦 Contenedor", opciones_contenedor)

    temperatura = st.number_input("🌡️ Temperatura (°C)", step=0.1, format="%.1f")

    rango_definido = -18.0 if "congelado" in contenedor.lower() else -0.5
    st.text_input("📏 Rango definido", value=f"{rango_definido}°C", disabled=True)

    diferencia = temperatura - rango_definido
    if abs(diferencia) < 1:
        valoracion = "Normal"
    elif abs(diferencia) < 3:
        valoracion = "Moderada"
    elif abs(diferencia) < 5:
        valoracion = "Alta"
    else:
        valoracion = "Crítica"
    st.text_input("🧮 Valoración", value=valoracion, disabled=True)

    st.info("📷 Para capturar una foto, usa tu cámara y súbela aquí.")
    foto = st.file_uploader("Sube la foto", type=["jpg", "jpeg", "png"])

    dispositivo = st.text_input("💻 Dispositivo", value=st.session_state.get("device_name", ""), disabled=True)

    if st.button("✅ Guardar registro"):
        nombre_archivo = f"{fecha_actual.replace('/', '-')}_{hora_actual.replace(':', '-')}.jpg"
        enlace_foto = ""

        if foto:
            carpeta_id = "11akWr6WaZON7qjw_4PGOvM3tLBq7pgYi"
            try:
                enlace_foto = subir_imagen_a_drive(foto, nombre_archivo, carpeta_id, st.secrets["gcp_service_account"])
                st.success(f"📁 Foto subida correctamente. [Ver imagen en Drive]({enlace_foto})")
            except Exception as e:
                st.error(f"❌ Error al subir la foto: {e}")

        fila = [
            fecha_actual,
            hora_actual,
            codigo,
            nombre,
            "",  # Almacén
            contenedor,
            temperatura,
            f"{rango_definido}°C",
            valoracion,
            enlace_foto,
            dispositivo
        ]
        hoja.append_row(fila)
        st.success("✅ Registro guardado correctamente")
