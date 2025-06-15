import platform
import subprocess
import os
from colorama import Fore, Style

def ejecutar():
    resultado = []
    sistema = platform.system()

    if sistema == "Windows":
        resultado.append("🛠️ Análisis resumido de servicios en Windows:\n")
        total = 0

        try:
            servicios = subprocess.check_output(
                'wmic service get Name,StartMode,State,PathName',
                shell=True, text=True, stderr=subprocess.DEVNULL
            ).splitlines()

            for s in servicios[1:]:
                parts = s.strip().split(None, 3)
                if len(parts) == 4:
                    total += 1

            resultado.append(f"{Fore.GREEN}🔢 Total de servicios: {total}{Style.RESET_ALL}")

        except Exception as e:
            resultado.append(f"[!] Error al listar servicios: {str(e)}")

    elif sistema == "Linux":
        resultado.append("🛠️ Servicios detectados en Linux:\n")
        try:
            servicios = subprocess.check_output(
                "systemctl list-units --type=service --all --no-pager --no-legend",
                shell=True, text=True
            ).splitlines()
            resultado.append(f"{Fore.GREEN}🔢 Servicios systemd detectados: {len(servicios)}{Style.RESET_ALL}")
        except Exception as e:
            resultado.append(f"[!] Error al obtener servicios systemd: {str(e)}")

        resultado.append("\n📁 Ejecutables encontrados en /etc/init.d:")
        try:
            ejecutables = []
            if os.path.isdir("/etc/init.d"):
                for s in os.listdir("/etc/init.d"):
                    path = os.path.join("/etc/init.d", s)
                    if os.access(path, os.X_OK):
                        ejecutables.append(s)
            resultado.append(f"{Fore.GREEN}🔹 Total: {len(ejecutables)}{Style.RESET_ALL}")
        except Exception as e:
            resultado.append(f"[!] Error al listar /etc/init.d: {str(e)}")

    else:
        resultado.append("Sistema operativo no soportado para este módulo.")

    return "\n".join(resultado)
