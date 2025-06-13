# modulos/network_shares.py
import platform
import subprocess


def ejecutar():
    resultado = []
    sistema = platform.system()
    resultado.append("🔗 Recursos compartidos en red detectados:\n")

    try:
        if sistema == "Windows":
            resultado.append("Usando: net share\n")
            salida = subprocess.check_output("net share", shell=True, text=True)
            resultado.append(salida.strip())

        elif sistema == "Linux":
            resultado.append("Usando: findmnt -t nfs,smbfs,cifs\n")
            try:
                salida = subprocess.check_output("findmnt -t nfs,smbfs,cifs", shell=True, text=True)
                resultado.append(salida.strip())
            except subprocess.CalledProcessError:
                resultado.append("No se detectaron recursos compartidos montados por NFS o CIFS.")

            resultado.append("\nComprobando /etc/fstab y montajes manuales conocidos...\n")
            try:
                fstab = subprocess.check_output("cat /etc/fstab | grep -iE 'nfs|cifs|smb'", shell=True, text=True)
                resultado.append(fstab.strip())
            except subprocess.CalledProcessError:
                resultado.append("No se encontraron entradas relevantes en /etc/fstab.")

        else:
            resultado.append("Sistema operativo no soportado para este módulo.")

    except Exception as e:
        resultado.append(f"[!] Error al obtener recursos compartidos: {str(e)}")

    return "\n".join(resultado)
