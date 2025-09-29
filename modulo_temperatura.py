from google.oauth2 import service_account
from google_auth_oauthlib.flow import Flow
from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseUpload
import streamlit as st
import pandas as pd
from datetime import datetime
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

def autenticar_usuario():
    if "google_creds" not in st.session_state:
        flow = Flow.from_client_config(
            {
                "web": {
                    "client_id": st.secrets["google_oauth"]["client_id"],
                    "client_secret": st.secrets["google_oauth"]["client_secret"],
                    "auth_uri": st.secrets["google_oauth"]["auth_uri"],
                    "token_uri": st.secrets["google_oauth"]["token_uri"],
                    "auth_provider_x509_cert_url": st.secrets["google_oauth"]["auth_provider_x509_cert_url"],
                    "redirect_uris": [st.secrets["google_oauth"]["redirect_uri"]],
                }
            },
            scopes=["https://www.googleapis.com/auth/drive.file"],
            redirect_uri=st.secrets["google_oauth"]["redirect_uri"]
        )

        auth_url, _ = flow.authorization_url(prompt="consent")
        st.markdown(f"[🔐 Autorizar acceso a Google Drive]({auth_url})")
        code = st.text_input("🔑 Pega aquí el código de autorización")
        if code:
            flow.fetch_token(code=code)
            st.session_state.google_creds = flow.credentials
            st.success("✅ Autenticado correctamente")

def subir_archivo_oauth(foto, nombre_archivo):
    creds = st.session_state.google_creds
    service = build("drive", "v3", credentials=creds)
    media = MediaIoBaseUpload(io.BytesIO(foto.read()), mimetype=foto.type)
    file_metadata = {"name": nombre_archivo}
    file = service.files().create(body=file_metadata, media_body=media, fields="id,webViewLink").execute()
    return file.get("webViewLink")

def mostrar_formulario_temperatura(conectar_sit_hh, cr_timezone):
    hoja = conectar_sit_hh().worksheet("TTemperatura")
    ahora = datetime.now(cr_timezone)
    fecha_actual = ahora.date()  # ✅ Se guarda como tipo fecha real
    hora_actual = ahora.strftime("%H:%M")

    st.text_input("📅 Fecha", value=fecha_actual.strftime("%d/%m/%Y"), disabled=True)
    st.text_input("⏰ Hora", value=hora_actual, disabled=True)

    codigo = st.session_state.codigo_empleado
    hoja_usuarios = conectar_sit_hh().worksheet("usuarios")
    datos_usuarios = hoja_usuarios.get_all_values()
    df_usuarios = pd.DataFrame(datos_usuarios[1:], columns=datos_usuarios[0])
    df_usuarios.columns = df_usuarios.columns.str.strip().str.lower()
    nombre = df_usuarios[df_usuarios["codigoempleado"].str.lower() == codigo.lower()]["nombreempleado"].values[0]

    st.text_input("👤 Usuario", value=codigo, disabled=True)
    st.text_input("🧑 Nombre de usuario", value=nombre, disabled=True)

    # Almacén
    opciones_almacen = ["Site Alajuela", "Site Cartago", "Site Curridabat", "Site Liberia", "Site SAVI"]
    almacen = st.selectbox("🏬 Almacén", opciones_almacen)

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

    autenticar_usuario()

    if st.button("✅ Guardar registro"):
        nombre_archivo = f"{fecha_actual.strftime('%d-%m-%Y')}_{hora_actual.replace(':', '-')}.jpg"
        enlace_foto = ""

        if foto:
            try:
                if "google_creds" in st.session_state:
                    enlace_foto = subir_archivo_oauth(foto, nombre_archivo)
                    st.success(f"📁 Foto subida correctamente. [Ver imagen en Drive]({enlace_foto})")
                else:
                    carpeta_id = "11akWr6WaZON7qjw_4PGOvM3tLBq7pgYi"
                    enlace_foto = subir_imagen_a_drive(foto, nombre_archivo, carpeta_id, st.secrets["gcp_service_account"])
                    st.success(f"📁 Foto subida con cuenta de servicio. [Ver imagen en Drive]({enlace_foto})")
            except Exception as e:
                st.error(f"❌ Error al subir la foto: {e}")

        fila = [
            fecha_actual,  # ✅ tipo fecha real
            hora_actual,
            codigo,
            nombre,
            almacen,
            contenedor,
            temperatura,
            f"{rango_definido}°C",
            valoracion,
            enlace_foto,
            dispositivo
        ]
        hoja.append_row(fila)
        st.success("✅ Registro guardado correctamente")
