# modulos/whoami_all.py

import subprocess
import platform

def ejecutar():
    try:
        if platform.system() == "Windows":
            resultado = subprocess.check_output("whoami /all", shell=True, stderr=subprocess.STDOUT, text=True)
        else:
            resultado = subprocess.check_output("id", shell=True, stderr=subprocess.STDOUT, text=True)
        return resultado
    except subprocess.CalledProcessError as e:
        return f"Error al ejecutar comando:\n{e.output}"
    except Exception as e:
        return f"Error inesperado: {str(e)}"
