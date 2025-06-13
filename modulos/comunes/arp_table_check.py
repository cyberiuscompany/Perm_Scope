# modulos/arp_table_check.py
import platform
import subprocess

def ejecutar():
    resultado = []
    sistema = platform.system()

    resultado.append("📶 Tabla ARP del sistema:\n")

    try:
        if sistema == "Windows":
            salida = subprocess.check_output("arp -a", shell=True, text=True)
            resultado.append(salida)

        elif sistema == "Linux":
            salida = subprocess.check_output("ip neigh show", shell=True, text=True)
            resultado.append(salida)
        else:
            resultado.append("Sistema operativo no soportado para este módulo.")

    except Exception as e:
        resultado.append(f"[!] Error al obtener tabla ARP: {str(e)}")

    return "\n".join(resultado)
