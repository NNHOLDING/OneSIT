import streamlit as st
import datetime
import pytz
import gspread
from google.oauth2.service_account import Credentials
import pandas as pd

cr_timezone = pytz.timezone("America/Costa_Rica")

def panel_exportar_ins():
    # Conexión con Google Sheets
    scope = ["https://spreadsheets.google.com/feeds",
             "https://www.googleapis.com/auth/drive"]
    creds = Credentials.from_service_account_info(st.secrets["gcp_service_account"], scopes=scope)
    client = gspread.authorize(creds)
    sheet = client.open_by_key("1PtUtGidnJkZZKW5CW4IzMkZ1tFk9dJLrGKe9vMwg0N0").worksheet("INS")

    st.title("📤 Exportar Registros INS")

    # Selectbox para fecha inicio y fin
    fecha_inicio = st.date_input("Fecha inicio", datetime.datetime.now(cr_timezone).date())
    fecha_fin = st.date_input("Fecha fin", datetime.datetime.now(cr_timezone).date())

    if st.button("Exportar a Excel"):
        # Leer todos los registros
        data = sheet.get_all_records()
        df = pd.DataFrame(data)

        # Convertir columna de fecha a datetime
        df["Fecha"] = pd.to_datetime(df["Fecha"], errors="coerce")

        # Filtrar por rango de fechas
        mask = (df["Fecha"].dt.date >= fecha_inicio) & (df["Fecha"].dt.date <= fecha_fin)
        df_filtrado = df.loc[mask]

        # Exportar a Excel
        nombre_archivo = f"registros_INS_{fecha_inicio}_a_{fecha_fin}.xlsx"
        df_filtrado.to_excel(nombre_archivo, index=False)

        # Descargar en Streamlit
        with open(nombre_archivo, "rb") as f:
            st.download_button(
                label="⬇️ Descargar Excel",
                data=f,
                file_name=nombre_archivo,
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            )