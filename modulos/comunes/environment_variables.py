from colorama import Fore, Style
import os
import platform


def ejecutar():
    resultado = []
    sistema = platform.system()
    resultado.append("🌱 Variables de entorno del sistema:\n")

    claves_importantes = [
        "USERNAME",
        "COMPUTERNAME",
        "USERDOMAIN",
        "USERPROFILE",
        "HOMEPATH",
        "PATH",
        "TEMP",
        "TMP",
        "SYSTEMROOT",
        "PROCESSOR_IDENTIFIER",
        "NUMBER_OF_PROCESSORS",
        "OS"
    ]

    try:
        for clave, valor in os.environ.items():
            if clave in claves_importantes:
                resultado.append(f"{Fore.GREEN}{clave} = {valor}{Style.RESET_ALL}")
            else:
                resultado.append(f"{clave} = {valor}")

        if sistema == "Linux":
            resultado.append("\n🔧 Variables adicionales de login shell:\n")
            try:
                from subprocess import check_output
                shell_vars = check_output("env", shell=True, text=True)
                resultado.append(shell_vars.strip())
            except Exception as e:
                resultado.append(f"[!] No se pudieron obtener variables con 'env': {str(e)}")

    except Exception as e:
        resultado.append(f"[!] Error al obtener variables de entorno: {str(e)}")

    return "\n".join(resultado)
