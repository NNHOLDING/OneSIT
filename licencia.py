import pandas as pd
from google_sheets import conectar_sit_hh
from datetime import datetime, timedelta

def validar_licencia(codigo_empleado):
    try:
        # Leer hoja usuarios
        hoja = conectar_sit_hh().worksheet("usuarios")
        datos = hoja.get_all_values()
        df = pd.DataFrame(datos[1:], columns=datos[0])
        # Normalizar nombres de columnas
        df.columns = df.columns.str.strip().str.lower()

        # 🔎 Depuración: imprime columnas para confirmar
        print("Columnas disponibles:", df.columns.tolist())

        # Buscar fila del usuario
        fila = df[df["codigoempleado"].str.strip().str.lower() == codigo_empleado.strip().lower()]
        if fila.empty:
            return False, "Usuario no encontrado en hoja usuarios"

        fila = fila.iloc[0]
        tipo = fila["tpo licencia"].strip()
        expiracion = fila["expiración licencia"].strip()

        # Caso licencia sin expiración
        if expiracion.lower() == "nunca":
            return True, f"Licencia {tipo} sin expiración"

        # Parsear fecha
        try:
            fecha_exp = datetime.strptime(expiracion, "%d/%m/%Y")
            hoy = datetime.now()

            if fecha_exp < hoy:
                return False, f"Licencia {tipo} expirada el {expiracion}"

            elif fecha_exp <= hoy + timedelta(days=15):
                dias_restantes = (fecha_exp - hoy).days
                return True, f"⚠️ Licencia {tipo} próxima a expirar en {dias_restantes} días (vence el {expiracion})"

            else:
                return True, f"Licencia {tipo} válida hasta {expiracion}"

        except ValueError:
            return False, f"Formato de fecha inválido en licencia: {expiracion}"

    except Exception as e:
        return False, f"Error validando licencia: {e}"
