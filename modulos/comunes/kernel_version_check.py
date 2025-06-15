# modulos/kernel_version_check.py
import platform
import subprocess
from colorama import Fore, Style

def ejecutar():
    resultado = []
    sistema = platform.system()

    resultado.append("🧬 Información del kernel y sistema:")

    try:
        if sistema == "Windows":
            version = platform.version()
            release = platform.release()
            resultado.append(f"Sistema operativo: Windows {release}")
            resultado.append(f"Versión del kernel: {Fore.GREEN}{version}{Style.RESET_ALL}")

            try:
                build_info = subprocess.check_output(
                    "systeminfo | findstr /B /C:\"OS Name\" /C:\"OS Version\"",
                    shell=True, text=True
                )
                resaltado = []
                for linea in build_info.strip().splitlines():
                    if ":" in linea:
                        clave, valor = linea.split(":", 1)
                        clave = clave.strip()
                        valor = valor.strip()
                        if "OS Version" in clave:
                            valor = f"{Fore.GREEN}{valor}{Style.RESET_ALL}"
                        linea = f"{clave}: {valor}"
                    resaltado.append(linea)
                resultado.append("\n📝 Detalles del sistema:")
                resultado.extend(resaltado)
                resultado.append("")  # ← salto de línea adicional
            except Exception:
                resultado.append("\n[!] No se pudo obtener información detallada del sistema.")

        elif sistema == "Linux":
            uname = subprocess.check_output("uname -a", shell=True, text=True)
            lsb = subprocess.getoutput("lsb_release -a")
            resultado.append(f"{uname.strip()}")
            resultado.append("\n📦 Distribución:")
            resultado.append(lsb)
        else:
            resultado.append("Sistema operativo no soportado.")

    except Exception as e:
        resultado.append(f"[!] Error al obtener información del kernel: {str(e)}")

    return "\n".join(resultado)
