import pandas as pd
from google_sheets import conectar_sit_hh
import streamlit as st
from datetime import datetime, timedelta
from defaults import defaults

def validar_licencia(codigo_empleado):
    try:
        hoja = conectar_sit_hh().worksheet("usuarios")
        datos = hoja.get_all_values()
        df = pd.DataFrame(datos[1:], columns=datos[0])
        df.columns = df.columns.str.strip().str.lower()

        # Mostrar columnas para depuración
        st.write("Columnas disponibles:", df.columns.tolist())

        fila = df[df["codigoempleado"].str.strip().str.lower() == codigo_empleado.strip().lower()]
        if fila.empty:
            st.error("⛔ Usuario no encontrado en hoja usuarios")
            return

        fila = fila.iloc[0]
        tipo = fila["tpo licencia"].strip()
        expiracion = fila["expiracion licencia"].strip()

        # Mostrar valor crudo leído
        st.write("Valor leído de expiracion licencia:", repr(expiracion))

        if expiracion.lower() == "nunca":
            st.success(f"Licencia {tipo} sin expiración")
            return

        # Intentar varios formatos de fecha
        fecha_exp = None
        formatos = ["%d/%m/%Y", "%d-%m-%Y", "%Y-%m-%d"]
        for fmt in formatos:
            try:
                fecha_exp = datetime.strptime(expiracion, fmt)
                st.write(f"Fecha interpretada correctamente con formato {fmt}: {fecha_exp}")
                break
            except ValueError:
                continue

        if fecha_exp is None:
            st.error(f"No se pudo interpretar la fecha: {expiracion}")
            return

        hoy = datetime.now()
        st.write(f"Hoy es: {hoy.strftime('%d/%m/%Y %H:%M:%S')}")

        if fecha_exp < hoy:
            st.error(f"Licencia {tipo} expirada el {expiracion}")
            # 🚪 Forzar cierre de sesión
            for key, value in defaults.items():
                st.session_state[key] = value
            st.stop()

        elif fecha_exp <= hoy + timedelta(days=15):
            dias_restantes = (fecha_exp - hoy).days
            st.warning(f"⚠️ Licencia {tipo} próxima a expirar en {dias_restantes} días (vence el {expiracion})")

        else:
            st.success(f"Licencia {tipo} válida hasta {expiracion}")

    except Exception as e:
        st.error(f"Error validando licencia: {e}")
