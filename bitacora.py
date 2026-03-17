import gspread
from oauth2client.service_account import ServiceAccountCredentials
from datetime import datetime

# Conexión a Google Sheets
def conectar_logenvios():
    scope = ["https://spreadsheets.google.com/feeds",
             "https://www.googleapis.com/auth/drive"]
    creds = ServiceAccountCredentials.from_json_keyfile_name("credenciales.json", scope)
    client = gspread.authorize(creds)
    # Abrir tu hoja por ID y seleccionar la pestaña LogEnvios
    return client.open_by_key("1PtUtGidnJkZZKW5CW4IzMkZ1tFk9dJLrGKe9vMwg0N0").worksheet("LogEnvios")

# Función para registrar logeos o acciones
def registrar_log(usuario, nombre_usuario, modulo, accion, dispositivo="Web"):
    hoja = conectar_logenvios()
    fecha = datetime.now().strftime("%Y-%m-%d")
    hora = datetime.now().strftime("%H:%M:%S")
    hoja.append_row([fecha, hora, usuario, nombre_usuario, modulo, accion, dispositivo])