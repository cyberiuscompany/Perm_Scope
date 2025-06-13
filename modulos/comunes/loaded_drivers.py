# modulos/mounted_drives.py
import platform
import subprocess
import re

def bytes_to_gb(size_str):
    try:
        return f"{int(size_str) / (1024 ** 3):.2f} GB"
    except:
        return size_str

def ejecutar():
    resultado = []
    sistema = platform.system()

    resultado.append("💽 Unidades montadas y discos detectados:\n")

    try:
        if sistema == "Windows":
            resultado.append("Usando: wmic logicaldisk get Name,FileSystem,Size,FreeSpace,Description\n")
            raw = subprocess.check_output("wmic logicaldisk get Name,FileSystem,Size,FreeSpace,Description", shell=True, text=True)
            lineas = [l.strip() for l in raw.strip().splitlines() if l.strip()]
            encabezados = lineas[0].split()
            resultado.append("\n" + " | ".join(["Description", "FileSystem", "FreeSpace", "Size", "Name"]))
            resultado.append("-" * 80)
            for linea in lineas[1:]:
                partes = re.split(r'\s{2,}', linea)
                if len(partes) == 5:
                    desc, fs, free, name, size = partes
                    resultado.append(f"{desc:20} | {fs:8} | {bytes_to_gb(free):>10} | {bytes_to_gb(size):>10} | {name}")

        elif sistema == "Linux":
            resultado.append("Usando: lsblk y df -h\n")
            salida_lsblk = subprocess.check_output("lsblk", shell=True, text=True)
            salida_df = subprocess.check_output("df -h", shell=True, text=True)
            resultado.append("\n[lsblk]\n")
            resultado.append(salida_lsblk)
            resultado.append("\n[df -h]\n")
            resultado.append(salida_df)

        else:
            resultado.append("Sistema operativo no soportado para este módulo.")

    except Exception as e:
        resultado.append(f"[!] Error al obtener unidades montadas: {str(e)}")

    return "\n".join(resultado)
