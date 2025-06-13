# modulos/kernel_version_check.py
import platform
import subprocess

def ejecutar():
    resultado = []
    sistema = platform.system()

    resultado.append("🧬 Información del kernel y sistema:")

    try:
        if sistema == "Windows":
            version = platform.version()
            release = platform.release()
            resultado.append(f"Sistema operativo: Windows {release}")
            resultado.append(f"Versión del kernel: {version}")

            try:
                build_info = subprocess.check_output("systeminfo | findstr /B /C:\"OS Name\" /C:\"OS Version\"", shell=True, text=True)
                resultado.append("\nDetalles del sistema:")
                resultado.append(build_info)
            except Exception:
                resultado.append("[!] No se pudo obtener información detallada del sistema.")

        elif sistema == "Linux":
            uname = subprocess.check_output("uname -a", shell=True, text=True)
            lsb = subprocess.getoutput("lsb_release -a")
            resultado.append(f"{uname.strip()}")
            resultado.append("\nDistribución:")
            resultado.append(lsb)
        else:
            resultado.append("Sistema operativo no soportado.")

    except Exception as e:
        resultado.append(f"[!] Error al obtener información del kernel: {str(e)}")

    return "\n".join(resultado)
