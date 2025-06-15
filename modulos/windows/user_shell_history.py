# modulos/user_shell_history.py
import platform
import os
import getpass


def ejecutar():
    resultado = []
    sistema = platform.system()
    usuario = getpass.getuser()

    resultado.append(f"📜 Historial de comandos de {usuario}\n")

    if sistema != "Windows":
        resultado.append("❌ Este módulo solo está disponible para sistemas Windows.")
        return "\n".join(resultado)

    try:
        perfil_powershell = os.path.expanduser(
            "~\\AppData\\Roaming\\Microsoft\\Windows\\PowerShell\\PSReadline\\ConsoleHost_history.txt"
        )
        if os.path.exists(perfil_powershell):
            resultado.append(f"\n[Historial PowerShell]\nArchivo: {perfil_powershell}\n")
            with open(perfil_powershell, "r", errors="ignore") as f:
                lineas = f.readlines()[-50:]
                resultado.extend(lineas if lineas else ["(Sin historial o vacío)"])
        else:
            resultado.append("No se encontró historial de PowerShell para este usuario.")
    except Exception as e:
        resultado.append(f"[!] Error al obtener historial de comandos: {str(e)}")

    return "\n".join([l.rstrip() for l in resultado])
