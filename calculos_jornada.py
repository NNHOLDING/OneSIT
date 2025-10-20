from datetime import datetime, timedelta
import pandas as pd
import streamlit as st

def redondear_media_hora(dt):
    minutos = dt.minute
    if minutos <= 15:
        return dt.replace(minute=0, second=0)
    elif minutos <= 45:
        return dt.replace(minute=30, second=0)
    else:
        dt += timedelta(hours=1)
        return dt.replace(minute=0, second=0)

def procesar_jornadas(conectar_funcion):
    st.write("🔍 Iniciando procesamiento de jornadas...")

    hoja_jornadas = conectar_funcion().worksheet("Jornadas")
    hoja_bd = conectar_funcion().worksheet("BD")

    datos_jornadas = hoja_jornadas.get_all_values()
    df_jornadas = pd.DataFrame(datos_jornadas[1:], columns=datos_jornadas[0])

    datos_bd = hoja_bd.get_all_values()
    df_bd = pd.DataFrame(datos_bd[1:], columns=datos_bd[0])

    # Convertir columna Hora de BD a tipo hora
    df_bd["Hora"] = pd.to_datetime(df_bd["Hora"], format="%H:%M:%S").dt.time
    df_bd = df_bd.sort_values("Hora")

    for i, fila in df_jornadas.iterrows():
        try:
            fila_id = i + 2  # índice real en hoja
            usuario = fila.get("usuario", "¿Sin nombre?")
            hora_inicio_raw = fila.get("Hora inicio", "").strip()
            hora_cierre_raw = fila.get("fecha cierre", "").strip()

            if not hora_inicio_raw or not hora_cierre_raw:
                st.write(f"⚠️ Fila {fila_id} ({usuario}): sin hora de inicio o cierre.")
                continue

            # Intentar parsear hora inicio y cierre
            try:
                hora_inicio = datetime.strptime(hora_inicio_raw, "%H:%M:%S")
            except:
                hora_inicio = datetime.strptime(hora_inicio_raw, "%H:%M")

            try:
                hora_cierre = datetime.strptime(hora_cierre_raw, "%H:%M:%S")
            except:
                hora_cierre = datetime.strptime(hora_cierre_raw, "%H:%M")

            # Ajuste si la hora de cierre es del día siguiente
            if hora_cierre < hora_inicio:
                hora_cierre += timedelta(days=1)

            inicio_redondeado = redondear_media_hora(hora_inicio)
            cierre_redondeado = redondear_media_hora(hora_cierre)

            # Buscar jornada estándar
            jornada_estandar = None
            for _, regla in df_bd.iterrows():
                if hora_inicio.time() <= regla["Hora"]:
                    jornada_estandar = float(regla["Jornada"])
                    break
            if jornada_estandar is None:
                jornada_estandar = 8

            duracion_real = (cierre_redondeado - inicio_redondeado).total_seconds() / 3600
            horas_extras = max(0, round(duracion_real - jornada_estandar, 2))

            # Mostrar trazas
            st.write(f"✅ Fila {fila_id} ({usuario}): {inicio_redondeado.strftime('%H:%M')} → {cierre_redondeado.strftime('%H:%M')} | Jornada={jornada_estandar} | Extras={horas_extras}")

            # Actualizar hoja
            hoja_jornadas.update_cell(fila_id, 6, inicio_redondeado.strftime("%H:%M"))  # Redondeo Inicio
            hoja_jornadas.update_cell(fila_id, 7, cierre_redondeado.strftime("%H:%M"))  # Redondeo Fin
            hoja_jornadas.update_cell(fila_id, 8, jornada_estandar)                     # Jornada
            hoja_jornadas.update_cell(fila_id, 9, horas_extras)                         # Total horas extras

        except Exception as e:
            st.write(f"❌ Error en fila {i+2} ({usuario}): {e}")
