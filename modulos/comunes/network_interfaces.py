# modulos/network_interfaces.py
import platform
import subprocess

def ejecutar():
    resultado = []
    sistema = platform.system()

    resultado.append("🌐 Información de interfaces de red:\n")

    try:
        if sistema == "Windows":
            salida = subprocess.check_output("ipconfig /all", shell=True, text=True)
            resultado.append(salida)

        elif sistema == "Linux":
            try:
                salida = subprocess.check_output("ip address show", shell=True, text=True)
            except subprocess.CalledProcessError:
                salida = subprocess.check_output("ifconfig -a", shell=True, text=True)
            resultado.append(salida)

        else:
            resultado.append("Sistema operativo no soportado para este módulo.")

    except Exception as e:
        resultado.append(f"[!] Error al obtener información de red: {str(e)}")

    return "\n".join(resultado)
