# modulos/password_policy.py
import platform
import subprocess


def ejecutar():
    resultado = []
    sistema = platform.system()

    resultado.append("🔐 Política de contraseñas del sistema:\n")

    try:
        if sistema == "Windows":
            resultado.append("Usando: net accounts\n")
            salida = subprocess.check_output("net accounts", shell=True, text=True)
            resultado.append(salida)

            resultado.append("\nPolítica local adicional desde secpol.msc no disponible en CLI.")

        elif sistema == "Linux":
            resultado.append("Usando: cat /etc/login.defs y chage -l\n")
            try:
                defs = subprocess.check_output("cat /etc/login.defs", shell=True, text=True)
                resultado.append("\n[Contenido de /etc/login.defs]\n")
                resultado.append(defs)
            except:
                resultado.append("No se pudo leer /etc/login.defs")

            resultado.append("\n[Política por usuario actual - chage -l]")
            try:
                salida = subprocess.check_output("chage -l $(whoami)", shell=True, text=True)
                resultado.append(salida)
            except:
                resultado.append("No se pudo ejecutar chage para el usuario actual.")

        else:
            resultado.append("Sistema operativo no soportado para este módulo.")

    except Exception as e:
        resultado.append(f"[!] Error al obtener política de contraseñas: {str(e)}")

    return "\n".join(resultado)
