# modulos/running_processes.py
import platform
import subprocess


def ejecutar():
    resultado = []
    sistema = platform.system()

    resultado.append("⚙️ Procesos en ejecución:\n")

    try:
        if sistema == "Windows":
            resultado.append("Usando: tasklist\n")
            salida = subprocess.check_output("tasklist", shell=True, text=True)
            resultado.append(salida)

        elif sistema == "Linux":
            resultado.append("Usando: ps aux\n")
            salida = subprocess.check_output("ps aux", shell=True, text=True)
            resultado.append(salida)

        else:
            resultado.append("Sistema operativo no soportado para este módulo.")

    except Exception as e:
        resultado.append(f"[!] Error al obtener procesos: {str(e)}")

    return "\n".join(resultado)
