# modulos/whoami_all.py

import subprocess
import platform
from colorama import init, Fore, Style
import re

init(autoreset=True)

def resaltar_salida(salida):
    resultado = []

    for linea in salida.splitlines():
        # Usuario actual y SID
        if re.match(r"^\s*\w.*\\.*\s+[Ss]-1-\d+-\d+", linea):
            resultado.append(Fore.GREEN + linea + Style.RESET_ALL)

        # Grupos de administradores
        elif "Administrators" in linea:
            resultado.append(Fore.GREEN + linea + Style.RESET_ALL)

        # Privilegios habilitados
        elif re.search(r"\bEnabled\b", linea) and "Privilege" in linea:
            resultado.append(Fore.GREEN + linea + Style.RESET_ALL)

        else:
            resultado.append(linea)

    return "\n".join(resultado)

def ejecutar():
    try:
        if platform.system() == "Windows":
            salida = subprocess.check_output("whoami /all", shell=True, stderr=subprocess.STDOUT, text=True)
            return resaltar_salida(salida)
        else:
            salida = subprocess.check_output("id", shell=True, stderr=subprocess.STDOUT, text=True)
            return salida
    except subprocess.CalledProcessError as e:
        return f"[!] Error al ejecutar comando:\n{e.output}"
    except Exception as e:
        return f"[!] Error inesperado: {str(e)}"
