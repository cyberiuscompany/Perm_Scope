# modulos/comunes/logged_in_users.py

import platform
import subprocess

def ejecutar():
    resultado = []
    sistema = platform.system()

    resultado.append("🧑‍💻 Sesiones de usuarios activas:\n")

    try:
        if sistema == "Windows":
            # Requiere CMD con permisos suficientes
            salida = subprocess.check_output("quser", shell=True, text=True)
            resultado.append("📍 Salida de 'quser':\n" + salida)

        elif sistema == "Linux":
            try:
                salida = subprocess.check_output("who", shell=True, text=True)
                resultado.append("📍 Salida de 'who':\n" + salida)
            except subprocess.CalledProcessError:
                salida = subprocess.check_output("w", shell=True, text=True)
                resultado.append("📍 Salida de 'w':\n" + salida)

        else:
            resultado.append("[!] Sistema operativo no soportado.")

    except Exception as e:
        resultado.append(f"[!] Error al obtener sesiones activas: {str(e)}")

    return "\n".join(resultado)
