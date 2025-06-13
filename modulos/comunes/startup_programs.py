# modulos/startup_programs.py
import platform
import subprocess
import os


def ejecutar():
    resultado = []
    sistema = platform.system()

    resultado.append("🚀 Programas de inicio automático:\n")

    try:
        if sistema == "Windows":
            resultado.append("Usando: wmic startup get Caption,Command,Location\n")
            salida = subprocess.check_output("wmic startup get Caption,Command,Location", shell=True, text=True)
            resultado.append(salida)

            resultado.append("\nRevisando claves de registro comunes de inicio (solo visual, no escritura):\n")
            claves = [
                "HKLM\\Software\\Microsoft\\Windows\\CurrentVersion\\Run",
                "HKCU\\Software\\Microsoft\\Windows\\CurrentVersion\\Run"
            ]
            for clave in claves:
                try:
                    reg = subprocess.check_output(f'reg query {clave}', shell=True, text=True)
                    resultado.append(f"\n[{clave}]\n{reg.strip()}\n")
                except subprocess.CalledProcessError:
                    resultado.append(f"\n[{clave}]\n(No se encontraron entradas o acceso denegado)\n")

        elif sistema == "Linux":
            resultado.append("Archivos de inicio del sistema y usuario:\n")
            rutas = [
                "~/.bashrc",
                "~/.profile",
                "~/.bash_profile",
                "~/.config/autostart/",
                "/etc/init.d/",
                "/etc/systemd/system/",
                "/etc/rc.local"
            ]
            for ruta in rutas:
                ruta_expandida = os.path.expanduser(ruta)
                if os.path.exists(ruta_expandida):
                    resultado.append(f"\n[{ruta_expandida}]\n")
                    if os.path.isdir(ruta_expandida):
                        for archivo in os.listdir(ruta_expandida):
                            resultado.append(f"- {archivo}")
                    else:
                        with open(ruta_expandida, 'r', errors='ignore') as f:
                            contenido = f.read()
                            resultado.append(contenido if contenido.strip() else "(Archivo vacío)")
                else:
                    resultado.append(f"\n[{ruta_expandida}] No existe.")

        else:
            resultado.append("Sistema operativo no soportado para este módulo.")

    except Exception as e:
        resultado.append(f"[!] Error al obtener programas de inicio: {str(e)}")

    return "\n".join(resultado)
