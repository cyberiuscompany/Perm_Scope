# modulos/antivirus_status.py
import platform
import subprocess
import psutil


def ejecutar():
    resultado = []
    sistema = platform.system()

    resultado.append("🛡️ Estado del antivirus:\n")

    try:
        if sistema == "Windows":
            # Parte 1: Intentar detección con PowerShell (SecurityCenter2)
            try:
                resultado.append("[🔍 Productos registrados por el sistema]")
                comando = [
                    "powershell",
                    "-Command",
                    "Get-CimInstance -Namespace root/SecurityCenter2 -ClassName AntivirusProduct | Select-Object displayName,productState,pathToSignedProductExe"
                ]
                salida = subprocess.check_output(comando, shell=True, text=True)
                resultado.append(salida.strip())
            except Exception as e:
                resultado.append(f"[!] No se pudo usar PowerShell con Get-CimInstance: {e}")

            # Parte 2: Detección basada en procesos comunes
            resultado.append("\n[🧠 Procesos sospechosos o relacionados con antivirus]")
            posibles = ["msmpeng.exe", "avastsvc.exe", "avgsvc.exe", "avp.exe", "savservice.exe", "ekrn.exe", "clamd.exe"]
            encontrados = []
            for proc in psutil.process_iter(['pid', 'name', 'exe']):
                if proc.info['name'] and proc.info['name'].lower() in posibles:
                    encontrados.append(f"PID {proc.info['pid']}: {proc.info['name']} ({proc.info['exe']})")
            if encontrados:
                resultado.extend(encontrados)
            else:
                resultado.append("❌ No se detectaron procesos de antivirus conocidos.")

        elif sistema == "Linux":
            resultado.append("[🔍 Buscando antivirus comunes instalados...]")
            comandos = {
                "ClamAV": "which clamscan",
                "ESET": "which esets_daemon",
                "Sophos": "which savdstatus",
                "Comodo": "which cmdscan"
            }
            detectados = []
            for nombre, cmd in comandos.items():
                try:
                    ruta = subprocess.check_output(cmd, shell=True, text=True).strip()
                    detectados.append(f"✅ {nombre} detectado en: {ruta}")
                except subprocess.CalledProcessError:
                    continue
            if detectados:
                resultado.extend(detectados)
            else:
                resultado.append("❌ No se detectó ningún antivirus instalado mediante rutas comunes.")

            # Parte 2: Revisar procesos relacionados
            resultado.append("\n[🧠 Procesos relacionados con antivirus]")
            keywords = ["clam", "eset", "av", "sophos", "comodo", "defender", "antivirus"]
            encontrados = []
            for proc in psutil.process_iter(['pid', 'name', 'exe']):
                name = (proc.info['name'] or "").lower()
                exe = (proc.info['exe'] or "").lower()
                if any(k in name or k in exe for k in keywords):
                    encontrados.append(f"PID {proc.info['pid']}: {proc.info['name']} ({proc.info['exe']})")
            if encontrados:
                resultado.extend(encontrados)
            else:
                resultado.append("❌ No se detectaron procesos relacionados con antivirus conocidos.")

        else:
            resultado.append("Sistema operativo no soportado para este módulo.")

    except Exception as e:
        resultado.append(f"[!] Error al verificar el estado del antivirus: {str(e)}")

    return "\n".join(resultado)
