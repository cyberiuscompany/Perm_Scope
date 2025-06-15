# modulos/firewall_check.py
import subprocess
import platform
import os
import re
from colorama import Fore, Style

def ejecutar():
    resultado = []
    sistema = platform.system()

    if sistema == "Windows":
        resultado.append("🛡️ Configuración del Firewall de Windows:\n")
        try:
            salida = subprocess.check_output('netsh advfirewall show allprofiles', shell=True, text=True)
            resultado.append(salida)

            # Extraer estados de cada perfil
            perfiles = {
                "Domain": "Desconocido",
                "Private": "Desconocido",
                "Public": "Desconocido"
            }

            for perfil in perfiles.keys():
                patron = rf"{perfil} Profile Settings:\s*-+\s*State\s+(ON|OFF)"
                match = re.search(patron, salida, re.IGNORECASE | re.DOTALL)
                if match:
                    estado = match.group(1).upper()
                    perfiles[perfil] = estado

            # Resumen
            resultado.append("\n📋 Resumen del estado del firewall por perfil:")
            for perfil, estado in perfiles.items():
                color = Fore.GREEN if estado == "ON" else Fore.RED
                resultado.append(f"  🔹 {perfil} Profile: {color}{estado}{Style.RESET_ALL}")

        except Exception as e:
            resultado.append(f"[!] Error al obtener la configuración del firewall: {str(e)}")
    
    elif sistema == "Linux":
        resultado.append("🛡️ Configuración de Firewall en Linux:\n")
        try:
            if os.path.exists("/usr/sbin/ufw"):
                estado = subprocess.check_output("sudo ufw status", shell=True, text=True)
                resultado.append("🔸 UFW (Uncomplicated Firewall):\n" + estado)
            elif os.path.exists("/usr/sbin/firewalld"):
                estado = subprocess.check_output("sudo firewall-cmd --state", shell=True, text=True)
                zonas = subprocess.check_output("sudo firewall-cmd --get-active-zones", shell=True, text=True)
                resultado.append("🔸 firewalld:\nEstado: " + estado + "\nZonas activas:\n" + zonas)
            elif os.path.exists("/sbin/iptables"):
                reglas = subprocess.check_output("sudo iptables -L", shell=True, text=True)
                resultado.append("🔸 iptables:\n" + reglas)
            else:
                resultado.append("No se detectó ningún firewall conocido instalado.")
        except Exception as e:
            resultado.append(f"[!] Error al obtener configuración del firewall: {str(e)}")

    else:
        resultado.append("Sistema operativo no soportado para este análisis.")

    return "\n".join(resultado)
