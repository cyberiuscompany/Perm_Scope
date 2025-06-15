# modulos/comunes/risky_logon_scripts_check.py

import platform
import subprocess
import os
import re

def expand_path(path):
    try:
        return os.path.expandvars(os.path.expanduser(path)).lower()
    except:
        return path.lower()

def ignorar_svchost(path):
    return "svchost.exe" in path and "system32" in path

def ejecutar():
    resultado = []
    sistema = platform.system()

    resultado.append("⚠️ Revisión de scripts de inicio de sesión y claves sospechosas:\n")

    try:
        if sistema == "Windows":
            claves_criticas = [
                r'HKCU\Software\Microsoft\Windows\CurrentVersion\Run',
                r'HKLM\Software\Microsoft\Windows\CurrentVersion\Run',
                r'HKLM\Software\Microsoft\Windows NT\CurrentVersion\Winlogon',
                r'HKCU\Environment'
            ]
            scripts_encontrados = []

            for clave in claves_criticas:
                try:
                    comando = f'reg query "{clave}"'
                    salida = subprocess.check_output(comando, shell=True, text=True, errors='ignore')
                    for linea in salida.strip().splitlines():
                        if "REG_" in linea:
                            partes = linea.strip().split("    ")
                            if len(partes) >= 3:
                                nombre = partes[-3].strip()
                                valor = expand_path(partes[-1])
                                if ignorar_svchost(valor):
                                    continue
                                if any(valor.endswith(ext) for ext in ['.bat', '.cmd', '.vbs', '.ps1', '.exe']) and os.path.exists(valor):
                                    scripts_encontrados.append(f"🔹 {clave}\\{nombre}: {valor}")
                except subprocess.CalledProcessError:
                    continue

            if scripts_encontrados:
                resultado.append("🔍 Scripts y valores sospechosos detectados:\n" + "\n".join(scripts_encontrados))
            else:
                resultado.append("✅ No se detectaron scripts de inicio sospechosos en el registro.")

        elif sistema == "Linux":
            archivos = [
                "/etc/profile", "/etc/bash.bashrc",
                os.path.expanduser("~/.bash_profile"),
                os.path.expanduser("~/.bashrc"),
                os.path.expanduser("~/.profile")
            ]
            carpetas = ["/etc/profile.d", "/etc/init.d"]
            scripts_encontrados = []

            # Archivos simples
            for archivo in archivos:
                if os.path.isfile(archivo):
                    with open(archivo, "r", errors="ignore") as f:
                        for linea in f:
                            posibles = re.findall(r'(/[^ \n\r\t;]+(?:\.sh|\.py|\.pl|\.bin|\.exe)?)', linea)
                            for ruta in posibles:
                                ruta_exp = expand_path(ruta)
                                if not ignorar_svchost(ruta_exp) and os.path.exists(ruta_exp):
                                    scripts_encontrados.append(f"🔹 {archivo}: {ruta_exp}")

            # Carpetas con scripts
            for carpeta in carpetas:
                if os.path.isdir(carpeta):
                    for root, _, files in os.walk(carpeta):
                        for file in files:
                            ruta = os.path.join(root, file)
                            if os.access(ruta, os.X_OK) and not ignorar_svchost(ruta):
                                scripts_encontrados.append(f"🔹 Script ejecutable: {ruta}")

            # Crontab del usuario
            try:
                cron = subprocess.check_output("crontab -l", shell=True, text=True, stderr=subprocess.DEVNULL)
                for linea in cron.strip().splitlines():
                    posibles = re.findall(r'(/[^ \n\r\t;]+(?:\.sh|\.py|\.pl|\.bin|\.exe)?)', linea)
                    for ruta in posibles:
                        ruta_exp = expand_path(ruta)
                        if not ignorar_svchost(ruta_exp) and os.path.exists(ruta_exp):
                            scripts_encontrados.append(f"🔹 Cronjob: {ruta_exp}")
            except:
                pass  # No hay crontab

            if scripts_encontrados:
                resultado.append("🔍 Scripts sospechosos detectados:\n" + "\n".join(scripts_encontrados))
            else:
                resultado.append("✅ No se detectaron scripts sospechosos en el inicio del sistema.")

        else:
            resultado.append("[!] Sistema operativo no soportado.")

    except Exception as e:
        resultado.append(f"[!] Error al detectar scripts: {str(e)}")

    return "\n".join(resultado)
