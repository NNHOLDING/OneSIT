import gspread
from oauth2client.service_account import ServiceAccountCredentials
import streamlit as st

# 🔗 Conexión con Google Sheets
def conectar_sit_hh():
    scope = [
        "https://spreadsheets.google.com/feeds",
        "https://www.googleapis.com/auth/drive"
    ]
    creds = ServiceAccountCredentials.from_json_keyfile_dict(
        st.secrets["gcp_service_account"], scope)
    client = gspread.authorize(creds)
    return client.open_by_url(
        "https://docs.google.com/spreadsheets/d/1PtUtGidnJkZZKW5CW4IzMkZ1tFk9dJLrGKe9vMwg0N0/edit"
    )