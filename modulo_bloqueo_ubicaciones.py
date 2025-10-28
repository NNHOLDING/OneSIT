import streamlit as st
import pandas as pd
from datetime import datetime

def mostrar_formulario_bloqueo(libro):
    st.subheader("🚫 Bloqueo de ubicaciones")

    # Autenticación
    usuario = st.text_input("👤 Usuario")
    contraseña = st.text_input("🔒 Contraseña", type="password")

    if not usuario or not contraseña:
        st.info("Ingresa tus credenciales para continuar.")
        return

    # Validar credenciales y permisos
    try:
        hoja_roles = libro.worksheet("Roles bloqueos")
        datos_roles = hoja_roles.get_all_values()
        df_roles = pd.DataFrame(datos_roles[1:], columns=datos_roles[0])
    except Exception as e:
        st.error(f"No se pudo cargar la hoja Roles bloqueos: {e}")
        return

    df_roles["Usuario"] = df_roles["Usuario"].str.strip()
    df_roles["Password"] = df_roles["Password"].str.strip()
    df_roles["Permisos"] = df_roles["Permisos"].str.strip().str.lower()
    df_roles["Rol"] = df_roles["Rol"].str.strip().str.lower()

    fila_usuario = df_roles[
        (df_roles["Usuario"] == usuario.strip()) &
        (df_roles["Password"] == contraseña.strip()) &
        (df_roles["Permisos"].str.contains("bloqueo"))
    ]

    if fila_usuario.empty:
        st.error("Credenciales inválidas o sin permiso de bloqueo.")
        return

    rol_usuario = fila_usuario.iloc[0]["Rol"].strip().lower()

    # Cargar motivos según rol
    try:
        hoja_motivos = libro.worksheet("Motivos")
        datos_motivos = hoja_motivos.get_all_values()
        df_motivos = pd.DataFrame(datos_motivos[1:], columns=datos_motivos[0])
    except Exception as e:
        st.error(f"No se pudo cargar la hoja Motivos: {e}")
        return

    df_motivos["Rol"] = df_motivos["Rol"].str.strip().str.lower()
    df_motivos["Codigo"] = df_motivos["Codigo"].str.strip()
    df_motivos["Motivo"] = df_motivos["Motivo"].str.strip()

    motivos_filtrados = df_motivos[df_motivos["Rol"] == rol_usuario]
    if motivos_filtrados.empty:
        st.warning("No hay motivos disponibles para tu rol.")
        return

    opciones_motivo = motivos_filtrados.apply(
        lambda row: f"{row['Codigo']} - {row['Motivo']}", axis=1
    ).drop_duplicates().tolist()

    motivo_seleccionado = st.selectbox("📝 Selecciona el motivo de bloqueo", opciones_motivo)
    codigo_motivo, texto_motivo = motivo_seleccionado.split(" - ", 1)

    # Formulario de ubicación
    ubicacion = st.text_input("📍 Ubicación a bloquear (ej. P01-1-1-1)").strip().upper()

    if st.button("🚫 Bloquear ubicación"):
        try:
            hoja_ubicaciones = libro.worksheet("Ubicaciones")
            datos = hoja_ubicaciones.get_all_values()
            encabezados = [col.strip() for col in datos[0]]
            df = pd.DataFrame(datos[1:], columns=encabezados)
        except Exception as e:
            st.error(f"No se pudo cargar la hoja Ubicaciones: {e}")
            return

        df["codigo"] = df.apply(
            lambda row: f"{str(row['Pasillo']).strip()}-{str(row['Tramo']).strip()}-{str(row['Nivel']).strip()}-{str(row['Posición']).strip()}",
            axis=1
        )
        df["codigo"] = df["codigo"].str.upper().str.strip()

        fila = df[df["codigo"] == ubicacion].index
        if fila.empty:
            st.error("La ubicación no existe.")
            return

        fila_idx = fila[0]
        hoja_ubicaciones.update_cell(fila_idx + 2, hoja_ubicaciones.find("Estado").col, "Bloqueado")
        hoja_ubicaciones.update_cell(fila_idx + 2, hoja_ubicaciones.find("Motivo bloqueo").col, texto_motivo)
        hoja_ubicaciones.update_cell(fila_idx + 2, hoja_ubicaciones.find("Código motivo").col, codigo_motivo)
        hoja_ubicaciones.update_cell(fila_idx + 2, hoja_ubicaciones.find("Registrado por").col, usuario)
        hoja_ubicaciones.update_cell(fila_idx + 2, hoja_ubicaciones.find("Fecha de asignación").col, datetime.now().strftime("%Y-%m-%d %H:%M:%S"))

        st.success(f"Ubicación {ubicacion} bloqueada exitosamente.")
