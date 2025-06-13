# modulos/open_ports_check.py
import platform
import subprocess


def ejecutar():
    resultado = []
    sistema = platform.system()

    resultado.append("🔌 Revisión de puertos abiertos en el sistema:\n")

    try:
        if sistema == "Windows":
            resultado.append("Usando: netstat -ano\n")
            salida = subprocess.check_output("netstat -ano", shell=True, text=True)
            resultado.append(salida)

        elif sistema == "Linux":
            try:
                resultado.append("Usando: ss -tulnp\n")
                salida = subprocess.check_output("ss -tulnp", shell=True, text=True)
                resultado.append(salida)
            except subprocess.CalledProcessError:
                resultado.append("Fallo 'ss', intentando con: netstat -tulnp\n")
                salida = subprocess.check_output("netstat -tulnp", shell=True, text=True)
                resultado.append(salida)

        else:
            resultado.append("Sistema operativo no soportado para este módulo.")

    except Exception as e:
        resultado.append(f"[!] Error al obtener puertos abiertos: {str(e)}")

    return "\n".join(resultado)
