from datetime import datetime, timedelta
import pandas as pd

def redondear_media_hora(dt):
    """
    Redondea una hora a la media hora más cercana.
    Ejemplo:
    - 03:14 → 03:00
    - 03:16 → 03:30
    - 03:46 → 04:00
    """
    minutos = dt.minute
    if minutos <= 15:
        return dt.replace(minute=0, second=0)
    elif minutos <= 45:
        return dt.replace(minute=30, second=0)
    else:
        dt += timedelta(hours=1)
        return dt.replace(minute=0, second=0)

def procesar_jornadas(conectar_funcion):
    hoja_jornadas = conectar_funcion().worksheet("Jornadas")
    hoja_bd = conectar_funcion().worksheet("BD")

    datos_jornadas = hoja_jornadas.get_all_values()
    df_jornadas = pd.DataFrame(datos_jornadas[1:], columns=datos_jornadas[0])

    datos_bd = hoja_bd.get_all_values()
    df_bd = pd.DataFrame(datos_bd[1:], columns=datos_bd[0])

    # Convertir columna "Hora" de BD a tipo hora
    df_bd["Hora"] = pd.to_datetime(df_bd["Hora"], format="%H:%M:%S").dt.time
    df_bd = df_bd.sort_values("Hora")

    for i, fila in df_jornadas.iterrows():
        try:
            # Validar que haya hora inicio y cierre
            if not fila["Hora inicio"] or not fila["fecha cierre"]:
                continue

            hora_inicio = datetime.strptime(fila["Hora inicio"], "%H:%M:%S")
            hora_cierre = datetime.strptime(fila["fecha cierre"], "%H:%M:%S")

            # Redondeos
            inicio_redondeado = redondear_media_hora(hora_inicio)
            cierre_redondeado = redondear_media_hora(hora_cierre)

            # Buscar jornada estándar en BD
            jornada_estandar = None
            for _, regla in df_bd.iterrows():
                if hora_inicio.time() <= regla["Hora"]:
                    jornada_estandar = float(regla["Jornada"])
                    break
            if jornada_estandar is None:
                jornada_estandar = 8  # valor por defecto

            # Calcular horas extras
            duracion_real = (cierre_redondeado - inicio_redondeado).total_seconds() / 3600
            horas_extras = max(0, round(duracion_real - jornada_estandar, 2))

            # Actualizar hoja
            hoja_jornadas.update_cell(i + 2, 6, inicio_redondeado.strftime("%H:%M"))  # Redondeo Inicio
            hoja_jornadas.update_cell(i + 2, 7, cierre_redondeado.strftime("%H:%M"))  # Redondeo Fin
            hoja_jornadas.update_cell(i + 2, 8, jornada_estandar)                     # Jornada
            hoja_jornadas.update_cell(i + 2, 9, horas_extras)                         # Total horas extras

        except Exception as e:
            print(f"Error en fila
