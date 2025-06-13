# modulos/user_shell_history.py
import platform
import os
import subprocess
import getpass


def ejecutar():
    resultado = []
    sistema = platform.system()
    usuario = getpass.getuser()

    resultado.append(f"📜 Historial de comandos de {usuario}\n")

    try:
        if sistema == "Windows":
            # En PowerShell, el historial se guarda con PSReadLine
            perfil_powershell = os.path.expanduser(f"~\\AppData\\Roaming\\Microsoft\\Windows\\PowerShell\\PSReadline\\ConsoleHost_history.txt")
            if os.path.exists(perfil_powershell):
                resultado.append(f"\n[Historial PowerShell]\nArchivo: {perfil_powershell}\n")
                with open(perfil_powershell, "r", errors="ignore") as f:
                    lineas = f.readlines()[-50:]
                    resultado.extend(lineas if lineas else ["(Sin historial o vacío)"])
            else:
                resultado.append("No se encontró historial de PowerShell para este usuario.")

        elif sistema == "Linux":
            shells = [".bash_history", ".zsh_history", ".sh_history"]
            home = os.path.expanduser("~")
            for sh in shells:
                ruta = os.path.join(home, sh)
                if os.path.exists(ruta):
                    resultado.append(f"\n[Historial: {sh}]\nArchivo: {ruta}\n")
                    with open(ruta, "r", errors="ignore") as f:
                        lineas = f.readlines()[-50:]
                        resultado.extend(lineas if lineas else ["(Sin historial o vacío)"])
        else:
            resultado.append("Sistema operativo no soportado para este módulo.")

    except Exception as e:
        resultado.append(f"[!] Error al obtener historial de comandos: {str(e)}")

    return "\n".join([l.rstrip() for l in resultado])
