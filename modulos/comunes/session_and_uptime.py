# modulos/session_and_uptime.py
import platform
import subprocess
import datetime
import psutil
from colorama import Fore, Style

def ejecutar():
    resultado = []
    sistema = platform.system()

    resultado.append("🔐 Sesiones activas y ⏱️ Tiempo desde el arranque:\n")

    try:
        if sistema == "Windows":
            # Usuarios activos (comando compatible con CMD)
            try:
                usuarios = subprocess.check_output("query user", shell=True, text=True)
                resultado.append(f"[Usuarios conectados]\n{usuarios.strip()}")
            except Exception as e:
                resultado.append(f"[!] No se pudo obtener usuarios conectados: {e}")

            # Uptime en formato legible
            boot_time = datetime.datetime.fromtimestamp(psutil.boot_time())
            ahora = datetime.datetime.now()
            tiempo_encendido = ahora - boot_time
            resultado.append(f"\n[Tiempo encendido]\nDesde: {boot_time.strftime('%Y-%m-%d %H:%M:%S')}")
            resultado.append(f"Duración: {str(tiempo_encendido).split('.')[0]}")

        elif sistema == "Linux":
            # Usuarios activos
            try:
                usuarios = subprocess.check_output("who", shell=True, text=True)
                resultado.append(f"[Usuarios conectados]\n{usuarios.strip()}")
            except Exception as e:
                resultado.append(f"[!] No se pudo obtener usuarios conectados: {e}")

            # Uptime legible
            boot_time = datetime.datetime.fromtimestamp(psutil.boot_time())
            ahora = datetime.datetime.now()
            tiempo_encendido = ahora - boot_time
            resultado.append(f"\n[Tiempo encendido]\nDesde: {boot_time.strftime('%Y-%m-%d %H:%M:%S')}")
            resultado.append(f"Duración: {str(tiempo_encendido).split('.')[0]}")

        else:
            resultado.append("❌ Sistema no soportado para este módulo.")

    except Exception as e:
        resultado.append(f"[!] Error general en el módulo: {e}")

    return "\n".join([Fore.GREEN + l + Style.RESET_ALL if l.strip() else "" for l in resultado])
