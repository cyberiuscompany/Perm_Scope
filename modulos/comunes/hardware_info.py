# comunes/hardware_info.py
import platform
import subprocess
from colorama import Fore, Style

def ejecutar():
    resultado = []
    sistema = platform.system()

    resultado.append("🖥️ Información del Hardware del Sistema:\n")

    try:
        if sistema == "Windows":
            resultado.append("📌 CPU y RAM:\n")
            cpu_info = subprocess.check_output("wmic cpu get Name,NumberOfCores,NumberOfLogicalProcessors", shell=True, text=True)
            ram_info = subprocess.check_output("wmic ComputerSystem get TotalPhysicalMemory", shell=True, text=True)
            resultado.append(cpu_info.strip())
            resultado.append(ram_info.strip())

            resultado.append("\n📦 Información adicional:\n")
            baseboard = subprocess.check_output("wmic baseboard get Manufacturer,Product", shell=True, text=True)
            bios = subprocess.check_output("wmic bios get Manufacturer,SMBIOSBIOSVersion", shell=True, text=True)
            resultado.append(baseboard.strip())
            resultado.append(bios.strip())

        elif sistema == "Linux":
            resultado.append("📌 CPU:\n")
            cpu_info = subprocess.check_output("lscpu", shell=True, text=True)
            resultado.append(cpu_info.strip())

            resultado.append("\n📦 RAM:\n")
            ram_info = subprocess.check_output("free -h", shell=True, text=True)
            resultado.append(ram_info.strip())

            resultado.append("\n🧬 Información adicional:\n")
            try:
                board = subprocess.check_output("sudo dmidecode -t baseboard", shell=True, text=True)
                bios = subprocess.check_output("sudo dmidecode -t bios", shell=True, text=True)
                resultado.append(board.strip())
                resultado.append(bios.strip())
            except Exception:
                resultado.append("🔒 No se pudo obtener información de BIOS/baseboard (requiere permisos).")

        else:
            resultado.append("❌ Sistema operativo no soportado.")

    except Exception as e:
        resultado.append(f"[!] Error al obtener información de hardware: {str(e)}")

    return "\n".join([Fore.GREEN + line + Style.RESET_ALL for line in resultado])
