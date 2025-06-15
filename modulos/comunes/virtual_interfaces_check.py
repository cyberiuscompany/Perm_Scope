import platform
import subprocess
import shutil
import re

def ejecutar():
    resultado = []
    sistema = platform.system()

    resultado.append("🔌 Interfaces virtuales detectadas:\n")

    try:
        if sistema == "Windows":
            try:
                # Usamos powershell directamente desde Python
                comando = [
                    "powershell",
                    "-Command",
                    "Get-NetAdapter | Select-Object Name, InterfaceDescription, Status, MacAddress, LinkSpeed | Format-Table -AutoSize"
                ]
                salida = subprocess.check_output(comando, text=True, stderr=subprocess.DEVNULL)
                interfaces = salida.strip()
                resultado.append("📋 Interfaces detectadas (Get-NetAdapter):\n" + interfaces)

                # Filtrado adicional de posibles interfaces virtuales por nombre
                virtual_keywords = ['virtual', 'vmware', 'loopback', 'vpn', 'hyper-v', 'fortinet', 'tap', 'tunnel', 'ndis']
                for linea in interfaces.splitlines():
                    if any(kw.lower() in linea.lower() for kw in virtual_keywords):
                        resultado.append(f"🔧 Posible interfaz virtual detectada: {linea.strip()}")

            except Exception as e:
                resultado.append(f"[!] Error en PowerShell: {str(e)}")

        elif sistema == "Linux":
            interfaces_detectadas = []

            # ifconfig o ip addr
            if shutil.which("ip"):
                salida = subprocess.check_output("ip -o link", shell=True, text=True)
                interfaces_detectadas = [line.split(":")[1].strip() for line in salida.strip().splitlines()]
            elif shutil.which("ifconfig"):
                salida = subprocess.check_output("ifconfig -a", shell=True, text=True)
                interfaces_detectadas = re.findall(r'^(\w+):', salida, re.MULTILINE)

            if interfaces_detectadas:
                resultado.append("📋 Interfaces detectadas:\n" + "\n".join(f" - {i}" for i in interfaces_detectadas))

            # Detectar interfaces virtuales conocidas
            for iface in interfaces_detectadas:
                if any(kw in iface.lower() for kw in ['lo', 'br', 'vir', 'veth', 'tap', 'tun', 'docker']):
                    resultado.append(f"🔧 Posible interfaz virtual: {iface}")

        else:
            resultado.append("[!] Sistema operativo no soportado.")

    except Exception as e:
        resultado.append(f"[!] Error al detectar interfaces: {str(e)}")

    return "\n".join(resultado)
