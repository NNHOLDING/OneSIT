import gspread
from google.oauth2.service_account import Credentials

def conectar_hoja_productividad():
    # 📌 ID de tu hoja de cálculo
    GOOGLE_SHEET_ID = "1PtUtGidnJkZZKW5CW4IzMkZ1tFk9dJLrGKe9vMwg0N0"

    # 📌 Datos de tu cuenta de servicio (ejemplo ficticio, reemplaza con los tuyos)
    service_account_info = {
        "type": "service_account",
        "project_id": "tu-proyecto",
        "private_key_id": "xxxx",
        "private_key": "-----BEGIN PRIVATE KEY-----\nTU_LLAVE\n-----END PRIVATE KEY-----\n",
        "client_email": "smartoneintelligence@onesit.iam.gserviceaccount.com",
        "client_id": "xxxx",
        "auth_uri": "https://accounts.google.com/o/oauth2/auth",
        "token_uri": "https://oauth2.googleapis.com/token",
        "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
        "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/smartoneintelligence%40onesit.iam.gserviceaccount.com"
    }

    # 🎯 Scopes recomendados
    scope = [
        "https://www.googleapis.com/auth/spreadsheets",
        "https://www.googleapis.com/auth/drive"
    ]

    try:
        # 🔐 Autenticación
        credentials = Credentials.from_service_account_info(service_account_info, scopes=scope)
        gc = gspread.authorize(credentials)

        # 📄 Abrir el libro
        libro = gc.open_by_key(GOOGLE_SHEET_ID)

        # 🧾 Buscar o crear la hoja "Productividad"
        nombre_hoja = "Productividad"
        hojas = libro.worksheets()
        nombres = [h.title for h in hojas]

        if nombre_hoja in nombres:
            sheet = libro.worksheet(nombre_hoja)
            print("✅ Hoja 'Productividad' encontrada.")
        else:
            sheet = libro.add_worksheet(title=nombre_hoja, rows="1000", cols="20")
            encabezados = [
                "ID", "Hora de registro", "Fecha", "Código empleado", "Nombre del empleado",
                "Placa", "Tipo de tarea", "Cantidad líneas - Unidades", "Cantidad líneas - Cajas",
                "Hora de inicio", "Hora de fin", "Eficiencia", "Hora fin de registro"
            ]
            sheet.insert_row(encabezados, index=1)
            print("✅ Hoja 'Productividad' creada con encabezados.")

        return sheet

    except Exception as e:
        print("❌ Error al conectar o preparar la hoja Productividad.")
        print(f"📛 Detalles técnicos: {e}")
        return None
