# modulos/network_interfaces.py
import platform
import subprocess
import re
from colorama import Fore, Style

def ejecutar():
    resultado = []
    sistema = platform.system()

    resultado.append("🌐 Información de interfaces de red:\n")

    try:
        if sistema == "Windows":
            salida = subprocess.check_output("ipconfig /all", shell=True, text=True)
        elif sistema == "Linux":
            try:
                salida = subprocess.check_output("ip address show", shell=True, text=True)
            except subprocess.CalledProcessError:
                salida = subprocess.check_output("ifconfig -a", shell=True, text=True)
        else:
            return "Sistema operativo no soportado para este módulo."

        # Resaltar IPv4, IPv6, DNS y DHCP
        salida_coloreada = []
        for linea in salida.splitlines():
            original = linea
            # IPv4
            linea = re.sub(r"(IPv4.+?:\s*)([\d\.]+)", r"\1" + Fore.GREEN + r"\2" + Style.RESET_ALL, linea, flags=re.IGNORECASE)
            # IPv6
            linea = re.sub(r"(IPv6.+?:\s*)([a-fA-F0-9:]+)", r"\1" + Fore.GREEN + r"\2" + Style.RESET_ALL, linea, flags=re.IGNORECASE)
            # DNS
            linea = re.sub(r"(DNS.+?:\s*)([\d\.]+)", r"\1" + Fore.GREEN + r"\2" + Style.RESET_ALL, linea, flags=re.IGNORECASE)
            # DHCP
            linea = re.sub(r"(DHCP.+?:\s*)([^\s]+)", r"\1" + Fore.GREEN + r"\2" + Style.RESET_ALL, linea, flags=re.IGNORECASE)

            salida_coloreada.append(linea)

        resultado.extend(salida_coloreada)

    except Exception as e:
        resultado.append(f"[!] Error al obtener información de red: {str(e)}")

    return "\n".join(resultado) + "\n"  # salto de línea limpio
