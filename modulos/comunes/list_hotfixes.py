import subprocess
import platform
import os

def ejecutar():
    resultado = []

    sistema = platform.system()

    if sistema == "Windows":
        resultado.append("HotFixes instalados:\n")
        try:
            qfe = subprocess.check_output("wmic qfe get Caption,Description,HotFixID,InstalledOn", shell=True, text=True)
            resultado.append(qfe)
        except Exception as e:
            resultado.append(f"[!] Error al obtener hotfixes: {str(e)}")

        try:
            expl_check = subprocess.check_output('systeminfo', shell=True, text=True)
            if any(word in expl_check.lower() for word in ["2000", "xp", "2003", "2008", "vista", "windows 7"]):
                resultado.append("\n[i] Posibles exploits disponibles (https://github.com/codingo/OSCP-2/blob/master/Windows/WinPrivCheck.bat)\n")

                checks = {
                    "KB2592799": "MS11-080 patch is NOT installed!",
                    "KB3143141": "MS16-032 patch is NOT installed!",
                    "KB2393802": "MS11-011 patch is NOT installed!",
                    "KB982799": "MS10-059 patch is NOT installed!",
                    "KB979683": "MS10-021 patch is NOT installed!",
                    "KB2305420": "MS10-092 patch is NOT installed!",
                    "KB981957": "MS10-073 patch is NOT installed!",
                    "KB4013081": "MS17-017 patch is NOT installed!",
                    "KB977165": "MS10-015 patch is NOT installed!",
                    "KB941693": "MS08-025 patch is NOT installed!",
                    "KB920958": "MS06-049 patch is NOT installed!",
                    "KB914389": "MS06-030 patch is NOT installed!",
                    "KB908523": "MS05-055 patch is NOT installed!",
                    "KB890859": "MS05-018 patch is NOT installed!",
                    "KB842526": "MS04-019 patch is NOT installed!",
                    "KB835732": "MS04-011 patch is NOT installed!",
                    "KB841872": "MS04-020 patch is NOT installed!",
                    "KB2975684": "MS14-040 patch is NOT installed!",
                    "KB3136041": "MS16-016 patch is NOT installed!",
                    "KB3057191": "MS15-051 patch is NOT installed!",
                    "KB2989935": "MS14-070 patch is NOT installed!",
                    "KB2778930": "MS13-005 patch is NOT installed!",
                    "KB2850851": "MS13-053 patch is NOT installed!",
                    "KB2870008": "MS13-081 patch is NOT installed!",
                }

                for kb, mensaje in checks.items():
                    try:
                        subprocess.check_output(f'wmic qfe get HotFixID | findstr /C:"{kb}"', shell=True, text=True)
                    except subprocess.CalledProcessError:
                        resultado.append(f"[!] {mensaje}")
        except Exception as e:
            resultado.append(f"[!] Error al comprobar sistema operativo para vulnerabilidades: {str(e)}")

    elif sistema == "Linux":
        resultado.append("📦 Paquetes instalados:\n")
        try:
            if os.path.exists("/usr/bin/dpkg"):
                listado = subprocess.check_output("dpkg -l | grep '^ii'", shell=True, text=True)
            elif os.path.exists("/usr/bin/rpm"):
                listado = subprocess.check_output("rpm -qa", shell=True, text=True)
            else:
                listado = "Gestor de paquetes no reconocido. No se puede listar hotfixes."
            resultado.append(listado)
        except Exception as e:
            resultado.append(f"[!] Error al obtener paquetes: {str(e)}")

        try:
            kernel = subprocess.check_output("uname -a", shell=True, text=True)
            resultado.append(f"\n🧠 Kernel actual:\n{kernel}")
        except:
            resultado.append("Error al obtener versión del kernel.")

    else:
        resultado.append("Sistema no reconocido para esta función.")

    return "\n".join(resultado)
