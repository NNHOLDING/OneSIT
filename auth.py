from google_sheets import conectar_sit_hh
import pandas as pd

# 🔍 Obtener nombre por código desde hoja "usuarios"
def obtener_nombre(codigo):
    hoja = conectar_sit_hh().worksheet("usuarios")
    datos = hoja.get_all_values()
    df = pd.DataFrame(datos[1:], columns=datos[0])
    df.columns = df.columns.str.strip().str.lower()
    fila = df[df["codigoempleado"].str.strip().str.lower() == codigo.strip().lower()]
    if not fila.empty:
        return fila.iloc[0]["nombreempleado"]
    return None

# 🔐 Validar credenciales desde hoja "usuarios"
def validar_login(usuario, contraseña):
    # Acceso maestro (opcional)
    if usuario == "Admin" and contraseña == "Administrador":
        return "admin", "Administrador"

    hoja = conectar_sit_hh().worksheet("usuarios")
    datos = hoja.get_all_values()
    df = pd.DataFrame(datos[1:], columns=datos[0])
    df.columns = df.columns.str.strip().str.lower()

    usuario = usuario.strip().lower()
    contraseña = contraseña.strip()

    fila = df[df["codigoempleado"].str.lower() == usuario]
    if not fila.empty:
        fila = fila.iloc[0]
        if fila["password"] == contraseña:
            # Usar columna "rol" si existe, de lo contrario asignar "estandar"
            rol = fila.get("rol", "estandar").strip().lower()
            return rol, fila["nombreempleado"]

    return None, None
