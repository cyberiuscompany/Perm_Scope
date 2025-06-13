# modulos/installed_software.py
import platform
import subprocess

def ejecutar():
    resultado = []
    sistema = platform.system()

    resultado.append("📦 Software Instalado:")

    try:
        if sistema == "Windows":
            resultado.append("\n🔍 Listando software mediante WMIC con detalles...")
            cmd = "wmic product get Name, Version, Vendor"
            salida = subprocess.check_output(cmd, shell=True, text=True, errors='ignore')
            resultado.append(salida.strip())

        elif sistema == "Linux":
            try:
                resultado.append("\n🔍 Listando paquetes con dpkg (Debian/Ubuntu)...")
                salida = subprocess.check_output("dpkg-query -W -f='${Package}\t${Version}\t${Maintainer}\n'", shell=True, text=True, errors='ignore')
                resultado.append(salida.strip())
            except subprocess.CalledProcessError:
                try:
                    resultado.append("\n🔍 Listando paquetes con rpm (RedHat/CentOS/Fedora)...")
                    salida = subprocess.check_output("rpm -qa --qf '%{NAME}\t%{VERSION}-%{RELEASE}\t%{VENDOR}\n'", shell=True, text=True, errors='ignore')
                    resultado.append(salida.strip())
                except subprocess.CalledProcessError:
                    resultado.append("❌ No se pudo detectar el gestor de paquetes compatible.")

        else:
            resultado.append("❌ Sistema operativo no compatible.")

    except Exception as e:
        resultado.append(f"[!] Error al listar software instalado: {str(e)}")

    return "\n".join(resultado)
