# modulos/comunes/timezone_and_ntp_check.py

import platform
import subprocess
import re

def ejecutar():
    resultado = []
    sistema = platform.system()
    resultado.append("🕒 Zona horaria y sincronización NTP:\n")

    try:
        if sistema == "Windows":
            # Obtener zona horaria
            try:
                zona = subprocess.check_output("tzutil /g", shell=True, text=True).strip()
                resultado.append(f"📍 Zona horaria actual: {zona}")
            except:
                resultado.append("❌ No se pudo obtener la zona horaria.")

            # Comprobar si el servicio de hora de Windows está activo
            try:
                status = subprocess.check_output("sc query w32time", shell=True, text=True)
                if "RUNNING" in status:
                    resultado.append("⏱️ Servicio NTP (w32time): ACTIVO")
                else:
                    resultado.append("⚪ Servicio NTP (w32time): INACTIVO o DETENIDO")
            except:
                resultado.append("❌ No se pudo consultar el servicio w32time.")

        elif sistema == "Linux":
            try:
                zona = subprocess.check_output("timedatectl | grep 'Time zone'", shell=True, text=True).strip()
                resultado.append(f"📍 {zona}")
            except:
                resultado.append("❌ No se pudo obtener la zona horaria.")

            try:
                salida = subprocess.check_output("timedatectl", shell=True, text=True)
                sincronizado = re.search(r"Synchronized:\s*(\w+)", salida)
                ntp_activo = re.search(r"NTP service:\s*(\w+)", salida)
                if sincronizado:
                    resultado.append(f"⏱️ Sincronizado: {sincronizado.group(1)}")
                if ntp_activo:
                    resultado.append(f"⚙️ Servicio NTP: {ntp_activo.group(1)}")
            except:
                resultado.append("❌ No se pudo consultar 'timedatectl'.")

        else:
            resultado.append("[!] Sistema operativo no soportado.")

    except Exception as e:
        resultado.append(f"[!] Error: {str(e)}")

    return "\n".join(resultado)
