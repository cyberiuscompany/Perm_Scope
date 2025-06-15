# modulos/comunes/virtual_interfaces_check.py

import platform
import subprocess
import re
import shutil

def ejecutar():
    resultado = []
    sistema = platform.system()

    resultado.append("🔌 Interfaces virtuales detectadas:\n")

    try:
        if sistema == "Windows":
            # Verificar si existe PowerShell
            powershell = shutil.which("powershell") or shutil.which("powershell.exe")
            if not powershell:
                raise Exception("PowerShell no encontrado en el sistema.")

            # Ejecutar correctamente con la ruta a powershell
            comando = [powershell, "-Command", "Get-NetAdapter | Format-Table -AutoSize"]
            salida = subprocess.check_output(comando, text=True, stderr=subprocess.DEVNULL)
            lineas = salida.splitlines()

            interfaces_virtuales = []
            for linea in lineas:
                if any(x in linea.lower() for x in [
                    "loopback", "vethernet", "vmware", "hyper-v", "tunnel", "tap", "virtual", "miniport", "fortinet"
                ]):
                    estado = "activa" if "up" in linea.lower() else "inactiva"
                    interfaces_virtuales.append(f"  - {linea.strip()} ({estado})")

            if interfaces_virtuales:
                resultado.append("📍 Interfaces virtuales encontradas en Windows:\n")
                resultado.extend(interfaces_virtuales)
            else:
                resultado.append("✅ No se encontraron interfaces virtuales en Windows.")

        elif sistema == "Linux":
            salida = subprocess.check_output("ip -o link show", shell=True, text=True)
            interfaces_virtuales = []

            for linea in salida.splitlines():
                nombre = re.search(r'\d+: ([^:]+):', linea)
                estado = "activa" if "state UP" in linea else "inactiva"

                if nombre:
                    iface = nombre.group(1)
                    if any(x in iface for x in [
                        "lo", "tun", "tap", "br", "virbr", "docker", "veth", "vmnet", "wlx", "bridge", "tailscale"
                    ]):
                        interfaces_virtuales.append(f"  - {iface} ({estado})")

            if interfaces_virtuales:
                resultado.append("📍 Interfaces virtuales encontradas en Linux:\n")
                resultado.extend(sorted(interfaces_virtuales))
            else:
                resultado.append("✅ No se encontraron interfaces virtuales en Linux.")

        else:
            resultado.append("[!] Sistema operativo no soportado.")

    except Exception as e:
        resultado.append(f"[!] Error al detectar interfaces virtuales: {str(e)}")

    return "\n".join(resultado)
