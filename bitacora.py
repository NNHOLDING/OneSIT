import gspread
from google.oauth2.service_account import Credentials
from datetime import datetime
import streamlit as st

def conectar_logenvios():
    scope = ["https://www.googleapis.com/auth/spreadsheets",
             "https://www.googleapis.com/auth/drive"]
    creds = Credentials.from_service_account_info(st.secrets["gcp_service_account"], scopes=scope)
    client = gspread.authorize(creds)
    return client.open_by_key("1PtUtGidnJkZZKW5CW4IzMkZ1tFk9dJLrGKe9vMwg0N0").worksheet("LogEnvios")

def registrar_log(usuario, nombre_usuario, modulo, accion, dispositivo="Web"):
    hoja = conectar_logenvios()
    fecha = datetime.now().strftime("%Y-%m-%d")
    hora = datetime.now().strftime("%H:%M:%S")
    hoja.append_row([fecha, hora, usuario, nombre_usuario, modulo, accion, dispositivo])
