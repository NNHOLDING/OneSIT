from google_sheets import conectar_sit_hh
import pandas as pd 
def validar_licencia(codigo_empleado):
    try:
        hoja = conectar_sit_hh().worksheet("usuarios")
        datos = hoja.get_all_values()
        df = pd.DataFrame(datos[1:], columns=datos[0])
        df.columns = df.columns.str.strip().str.lower()

        fila = df[df["codigoempleado"].str.strip().str.lower() == codigo_empleado.strip().lower()]
        if fila.empty:
            return False, "⛔ Usuario no encontrado en hoja usuarios"

        fila = fila.iloc[0]
        tipo = fila["tpo licencia"].strip()
        expiracion = fila["expiracion licencia"].strip()

        # Mostrar lectura de campos
        st.write("Licencia encontrada:", {"tipo": tipo, "expiracion": expiracion})

        if expiracion.lower() == "nunca":
            return True, f"Licencia {tipo} sin expiración"

        # Intentar varios formatos
        fecha_exp = None
        for fmt in ("%d/%m/%Y", "%d-%m-%Y", "%Y-%m-%d"):
            try:
                fecha_exp = datetime.strptime(expiracion, fmt)
                break
            except ValueError:
                continue

        if fecha_exp is None:
            return False, f"No se pudo interpretar la fecha: {expiracion}"

        hoy = datetime.now()

        if fecha_exp < hoy:
            return False, f"Licencia {tipo} expirada el {expiracion}"
        elif fecha_exp <= hoy + timedelta(days=15):
            dias_restantes = (fecha_exp - hoy).days
            return True, f"⚠️ Licencia {tipo} próxima a expirar en {dias_restantes} días (vence el {expiracion})"
        else:
            return True, f"Licencia {tipo} válida hasta {expiracion}"

    except Exception as e:
        return False, f"Error validando licencia: {e}"
