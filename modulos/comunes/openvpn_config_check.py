# modulos/comunes/openvpn_config_check.py

import platform
import subprocess
import os

def ejecutar():
    resultado = []
    sistema = platform.system()
    resultado.append("📦 Búsqueda de configuraciones y archivos de VPN (OpenVPN, WireGuard, etc.):\n")

    extensiones_interes = [".ovpn", ".tblk", ".conf", ".ovpn12", ".ovpn22", ".crt", ".key", ".pem"]

    try:
        rutas_detectadas = []

        if sistema == "Windows":
            # Buscar en unidades locales principales
            unidades = ["C:\\", "D:\\"] if os.path.exists("D:\\") else ["C:\\"]
            for unidad in unidades:
                try:
                    for ext in extensiones_interes:
                        comando = f'where /r "{unidad}" *{ext}'
                        salida = subprocess.check_output(comando, shell=True, text=True, stderr=subprocess.DEVNULL)
                        rutas_detectadas.extend(salida.strip().splitlines())
                except subprocess.CalledProcessError:
                    continue  # Puede no encontrar resultados

        elif sistema == "Linux":
            try:
                # Usar 'find' para buscar ficheros con extensiones relacionadas
                comandos = [
                    f"find /etc -type f \\( {' -o '.join([f'-iname *{ext}' for ext in extensiones_interes])} \\) 2>/dev/null",
                    f"find /home -type f \\( {' -o '.join([f'-iname *{ext}' for ext in extensiones_interes])} \\) 2>/dev/null",
                    f"find /usr -type f \\( {' -o '.join([f'-iname *{ext}' for ext in extensiones_interes])} \\) 2>/dev/null"
                ]
                for cmd in comandos:
                    salida = subprocess.check_output(cmd, shell=True, text=True)
                    rutas_detectadas.extend(salida.strip().splitlines())
            except Exception as e:
                resultado.append(f"[!] Error al ejecutar búsquedas en Linux: {str(e)}")

        else:
            resultado.append("[!] Sistema operativo no soportado.")
            return "\n".join(resultado)

        if rutas_detectadas:
            resultado.append("🔍 Archivos de configuración VPN encontrados:\n")
            for ruta in sorted(set(rutas_detectadas)):
                resultado.append(f"  - {ruta}")
        else:
            resultado.append("✅ No se encontraron archivos de configuración VPN.")

    except Exception as e:
        resultado.append(f"[!] Error durante la búsqueda de archivos VPN: {str(e)}")

    return "\n".join(resultado)
