# modulos/mounted_drives.py
import platform
import subprocess


def ejecutar():
    resultado = []
    sistema = platform.system()

    resultado.append("💽 Unidades montadas y discos detectados:\n")

    try:
        if sistema == "Windows":
            resultado.append("Usando: wmic logicaldisk get Name,FileSystem,Size,FreeSpace,Description\n")
            salida = subprocess.check_output("wmic logicaldisk get Name,FileSystem,Size,FreeSpace,Description", shell=True, text=True)
            resultado.append(salida)

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
