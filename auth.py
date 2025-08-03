from google_sheets import conectar_sit_hh

# 🔍 Obtener nombre por código desde hoja "Empleados"
def obtener_nombre(codigo):
    hoja = conectar_sit_hh().worksheet("Empleados")
    datos = hoja.get_all_values()
    for fila in datos:
        if fila[0] == codigo:
            return fila[1]
    return None

# 🔐 Validar credenciales
def validar_login(usuario, contraseña):
    if usuario == "Admin" and contraseña == "Administrador":
        return "admin", "Administrador"
    elif contraseña == f"numar{usuario}":
        nombre = obtener_nombre(usuario)
        if nombre:
            return "estandar", nombre
    return None, None