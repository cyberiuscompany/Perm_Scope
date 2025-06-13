# modulos/insecure_services.py
import platform
import subprocess
import os

def ejecutar():
    resultado = []
    sistema = platform.system()

    if sistema == "Windows":
        resultado.append("🛠️ Servicios en Windows:\n")
        try:
            servicios = subprocess.check_output(
                'wmic service get Name,StartMode,State,PathName',
                shell=True, text=True, stderr=subprocess.DEVNULL
            ).splitlines()
            for s in servicios[1:]:
                parts = s.strip().split(None, 3)
                if len(parts) == 4:
                    nombre, modo, estado, ruta = parts
                    if ' ' in ruta and not ruta.startswith('"'):
                        resultado.append(f"[!] Servicio: {nombre}\n    Estado: {estado}\n    Modo de inicio: {modo}\n    Ruta: {ruta}\n")
        except Exception as e:
            resultado.append(f"[!] Error al listar servicios: {str(e)}")

    elif sistema == "Linux":
        resultado.append("🛠️ Servicios en Linux (systemd):\n")
        try:
            servicios = subprocess.check_output("systemctl list-units --type=service --all", shell=True, text=True)
            resultado.append(servicios)
        except Exception as e:
            resultado.append(f"[!] Error al obtener servicios con systemd: {str(e)}")

        resultado.append("\n🔍 Servicios en /etc/init.d:\n")
        try:
            if os.path.isdir("/etc/init.d"):
                scripts = os.listdir("/etc/init.d")
                for s in scripts:
                    path = os.path.join("/etc/init.d", s)
                    if os.access(path, os.X_OK):
                        resultado.append(f"{s} (ejecutable)")
            else:
                resultado.append("No se encontró /etc/init.d")
        except Exception as e:
            resultado.append(f"[!] Error al listar /etc/init.d: {str(e)}")

    else:
        resultado.append("Sistema no soportado para este análisis.")

    return "\n".join(resultado)