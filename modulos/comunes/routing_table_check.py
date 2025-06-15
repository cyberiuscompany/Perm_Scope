# modulos/comunes/routing_table_check.py

import platform
import subprocess
import re

# Colores ANSI
GREEN = "\033[92m"
CYAN = "\033[96m"
RESET = "\033[0m"
BOLD = "\033[1m"

def resaltar_lineas(lineas):
    resaltadas = []
    for linea in lineas.splitlines():
        if "0.0.0.0" in linea and "Gateway" not in linea:
            resaltadas.append(f"{BOLD}{GREEN}{linea}{RESET}")  # Gateway por defecto
        elif "Interface List" in linea or "Active Routes" in linea or "Persistent Routes" in linea:
            resaltadas.append(f"{BOLD}{CYAN}{linea}{RESET}")
        elif re.search(r"VMware|Fortinet|Wi-Fi|Ethernet", linea):
            resaltadas.append(f"{GREEN}{linea}{RESET}")  # Interfaces relevantes
        else:
            resaltadas.append(linea)
    return "\n".join(resaltadas)

def ejecutar():
    resultado = []
    sistema = platform.system()

    resultado.append("🛣️ Tabla de rutas del sistema:\n")

    try:
        if sistema == "Windows":
            salida = subprocess.check_output("route print", shell=True, text=True)
        elif sistema == "Linux":
            salida = subprocess.check_output("ip route show", shell=True, text=True)
        else:
            return "[!] Sistema operativo no soportado."

        salida_coloreada = resaltar_lineas(salida)
        resultado.append(salida_coloreada)

    except Exception as e:
        resultado.append(f"[!] Error al obtener la tabla de rutas: {str(e)}")

    return "\n".join(resultado)
