import platform
import subprocess
import os

def ejecutar():
    resultado = []
    sistema = platform.system()
    resultado.append("📦 Búsqueda de configuraciones y archivos de VPN (OpenVPN, WireGuard, etc.):\n")

    extensiones_interes = [".ovpn", ".tblk", ".conf", ".ovpn12", ".ovpn22", ".crt", ".key", ".pem"]
    rutas_detectadas = []

    try:
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
                    continue  # Puede no encontrar resultados sin ser error real

        elif sistema == "Linux":
            # Buscar usando 'find' sin provocar errores si no encuentra nada
            comandos = [
                f"find /etc -type f \\( {' -o '.join([f'-iname *{ext}' for ext in extensiones_interes])} \\)",
                f"find /home -type f \\( {' -o '.join([f'-iname *{ext}' for ext in extensiones_interes])} \\)",
                f"find /usr -type f \\( {' -o '.join([f'-iname *{ext}' for ext in extensiones_interes])} \\)"
            ]
            for cmd in comandos:
                proc = subprocess.run(cmd, shell=True, text=True, capture_output=True)
                if proc.returncode == 0 and proc.stdout.strip():
                    rutas_detectadas.extend(proc.stdout.strip().splitlines())

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
