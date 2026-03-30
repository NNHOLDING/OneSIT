import pandas as pd
from google_sheets import conectar_sit_hh
import streamlit as st
from datetime import datetime, timedelta

def validar_licencia(codigo_empleado):
    try:
        hoja = conectar_sit_hh().worksheet("usuarios")
        datos = hoja.get_all_values()
        df = pd.DataFrame(datos[1:], columns=datos[0])
        df.columns = df.columns.str.strip().str.lower()

        fila = df[df["codigoempleado"].str.strip().str.lower() == codigo_empleado.strip().lower()]
        if fila.empty:
            return False, "Usuario no encontrado"

        fila = fila.iloc[0]
        tipo = fila.get("tpo licencia", "Desconocida")
        expiracion = fila.get("expiración licencia", "").strip()

        if expiracion.lower() == "nunca":
            return True, f"Licencia {tipo} sin expiración"

        try:
            fecha_exp = datetime.strptime(expiracion, "%d/%m/%Y")
            hoy = datetime.now()

            if fecha_exp < hoy:
                return False, f"Licencia {tipo} expirada el {expiracion}"

            elif fecha_exp <= hoy + timedelta(days=15):
                return True, f"⚠️ Licencia {tipo} próxima a expirar el {expiracion}"

            else:
                return True, f"Licencia {tipo} válida hasta {expiracion}"

        except:
            return False, "Formato de fecha inválido"

    except Exception as e:
        return False, f"Error validando licencia: {e}"