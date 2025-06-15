# modulos/antivirus_status.py
import platform
import subprocess
import psutil
from colorama import Fore, Style

def ejecutar():
    resultado = []
    sistema = platform.system()

    resultado.append("🛡️ Estado del antivirus:\n")

    try:
        if sistema == "Windows":
            # Parte 1: Detección con PowerShell (SecurityCenter2)
            try:
                resultado.append("[🔍 Productos registrados por el sistema]")
                comando = [
                    "powershell",
                    "-Command",
                    "Get-CimInstance -Namespace root/SecurityCenter2 -ClassName AntivirusProduct | Select-Object displayName,productState,pathToSignedProductExe"
                ]
                salida = subprocess.check_output(comando, shell=True, text=True)
                for linea in salida.strip().splitlines():
                    if "displayName" in linea or "-----------" in linea:
                        resultado.append(linea)
                    elif linea.strip():
                        partes = linea.split(None, 2)
                        if len(partes) == 3:
                            nombre, estado, ruta = partes
                            resultado.append(f"{Fore.GREEN}{nombre}{Style.RESET_ALL} {estado} {ruta}")
                        else:
                            resultado.append(linea)
            except Exception as e:
                resultado.append(f"[!] No se pudo usar PowerShell con Get-CimInstance: {e}")

            # Parte 2: Procesos comunes de antivirus
            resultado.append("\n[🧠 Procesos sospechosos o relacionados con antivirus]")
            posibles = [
                "msmpeng.exe", "avastsvc.exe", "avgsvc.exe", "avp.exe", "savservice.exe", "ekrn.exe", "clamd.exe",
                "mcshield.exe", "nortonsecurity.exe", "symantec.exe", "f-secure.exe", "bitdefender.exe",
                "esets_daemon.exe", "k7av.exe", "trendmicro.exe", "zillya.exe", "panda_cloud_antivirus.exe",
                "qihoo360tray.exe", "webroot.exe", "drweb.exe", "trustport.exe", "sophosfs.exe", "emsisoft.exe",
                "defendpoint.exe", "scanner.exe", "antivir.exe", "bdagent.exe", "mbam.exe", "mbae.exe",
                "avgnt.exe", "vshieldscanner.exe", "mfevtps.exe", "ashdisp.exe", "ashserv.exe", "ashwebsv.exe",
                "ashmaisv.exe", "kavtray.exe", "klnagent.exe", "fsgk32.exe", "fsdfwd.exe", "fsav32.exe",
                "fsorsp.exe", "fsaua.exe", "vsserv.exe", "spidernt.exe", "dwengine.exe", "cavtray.exe",
                "antimalware.exe", "nod32krn.exe", "avengine.exe", "avguard.exe"
            ]
            encontrados = []
            for proc in psutil.process_iter(['pid', 'name', 'exe']):
                if proc.info['name'] and proc.info['name'].lower() in posibles:
                    encontrados.append(f"{Fore.GREEN}PID {proc.info['pid']}: {proc.info['name']} ({proc.info['exe']}){Style.RESET_ALL}")
            if encontrados:
                resultado.extend(encontrados)
            else:
                resultado.append("❌ No se detectaron procesos de antivirus conocidos.")

        elif sistema == "Linux":
            resultado.append("[🔍 Buscando antivirus comunes instalados...]")
            comandos = {
                "ClamAV": "which clamscan", "ESET": "which esets_daemon", "Sophos": "which savdstatus",
                "Comodo": "which cmdscan", "AVG": "which avgscan", "Avast": "which avast",
                "F-Secure": "which fsav", "Bitdefender": "which bdscan", "Dr.Web": "which drweb",
                "Panda": "which panda", "Kaspersky": "which kav", "TrendMicro": "which trend",
                "Webroot": "which wrscan", "Norton": "which norton", "McAfee": "which mcafee",
                "Zillya": "which zillya", "Qihoo360": "which qihoo360", "TrustPort": "which trustport",
                "Emsisoft": "which emsisoft", "Defenx": "which defenx", "Avira": "which antivir",
                "Spybot": "which spybot", "ZoneAlarm": "which zonealarm", "Adaware": "which adaware",
                "Immunet": "which immunet", "Fortinet": "which forticlient", "CrowdStrike": "which falcon-sensor",
                "SentinelOne": "which sentinelctl", "Cybereason": "which cybereason", "Malwarebytes": "which mbam",
                "PC Matic": "which pcmatic", "TotalAV": "which totalav", "BullGuard": "which bullguard",
                "Kingsoft": "which kingsoft", "Rising": "which rising", "IObit": "which iobit",
                "Tencent": "which tencent", "QiAnXin": "which qianxin", "MaxSecure": "which maxsecure",
                "GData": "which gdata", "Vba32": "which vba32", "Norman": "which norman",
                "Prevx": "which prevx", "Armor2net": "which armor2net", "AhnLab": "which ahnlab",
                "Jiangmin": "which jiangmin"
            }
            detectados = []
            for nombre, cmd in comandos.items():
                try:
                    ruta = subprocess.check_output(cmd, shell=True, text=True).strip()
                    detectados.append(f"{Fore.GREEN}✅ {nombre} detectado en: {ruta}{Style.RESET_ALL}")
                except subprocess.CalledProcessError:
                    continue
            if detectados:
                resultado.extend(detectados)
            else:
                resultado.append("❌ No se detectó ningún antivirus instalado mediante rutas comunes.")

            keywords = [
                "clam", "eset", "avg", "avast", "avp", "mcafee", "norton", "symantec", "bitdefender", "f-secure",
                "sophos", "panda", "defender", "zillya", "qihoo", "trustport", "webroot", "drweb", "emsisoft", "trend",
                "spybot", "adaware", "fortinet", "crowdstrike", "sentinelone", "cybereason", "pcm", "bullguard", "kingsoft",
                "rising", "iobit", "tencent", "qianxin", "maxsecure", "gdata", "vba32", "norman", "prevx", "armor2net",
                "ahnlab", "jiangmin", "malwarebytes", "totalav", "avira"
            ]
            encontrados = []
            for proc in psutil.process_iter(['pid', 'name', 'exe']):
                name = (proc.info['name'] or "").lower()
                exe = (proc.info['exe'] or "").lower()
                if any(k in name or k in exe for k in keywords):
                    encontrados.append(f"{Fore.GREEN}PID {proc.info['pid']}: {proc.info['name']} ({proc.info['exe']}){Style.RESET_ALL}")
            if encontrados:
                resultado.extend(encontrados)
            else:
                resultado.append("❌ No se detectaron procesos relacionados con antivirus conocidos.")

        else:
            resultado.append("Sistema operativo no soportado para este módulo.")

    except Exception as e:
        resultado.append(f"[!] Error al verificar el estado del antivirus: {str(e)}")

    return "\n".join(resultado) + "\n"  # <-- Salto de línea limpio al final
