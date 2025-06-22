import platform
import subprocess
import os
from collections import OrderedDict


def ejecutar():
    resultado = []
    sistema = platform.system()

    resultado.append("🚀 Programas de inicio automático:\n")

    try:
        if sistema == "Windows":
            resultado.append("🔹 Programas registrados en WMIC:\n")
            raw = subprocess.check_output("wmic startup get Caption,Command,Location", shell=True, text=True)
            lineas = raw.strip().splitlines()
            programas = OrderedDict()

            # Detectar posiciones de columnas
            header = lineas[0]
            idx_caption = header.find("Caption")
            idx_command = header.find("Command")
            idx_location = header.find("Location")

            for linea in lineas[1:]:
                if not linea.strip():
                    continue
                caption = linea[idx_caption:idx_command].strip()
                command = linea[idx_command:idx_location].strip()
                location = linea[idx_location:].strip()

                key = f"{caption} | {command}"
                if key not in programas:
                    programas[key] = location

            for item, location in programas.items():
                resultado.append(f"  - {item}")

            # Revisar claves del registro
            resultado.append("\n🗂️ Revisando claves de registro comunes de inicio (solo visual, no escritura):\n")
            claves = [
                "HKLM\\Software\\Microsoft\\Windows\\CurrentVersion\\Run",
                "HKCU\\Software\\Microsoft\\Windows\\CurrentVersion\\Run"
            ]
            for clave in claves:
                try:
                    reg = subprocess.check_output(f'reg query {clave}', shell=True, text=True)
                    resultado.append(f"\n[{clave}]\n{reg.strip()}\n")
                except subprocess.CalledProcessError:
                    resultado.append(f"\n[{clave}]\n(No se encontraron entradas o acceso denegado)\n")
elif sistema == "Linux":
    resultado.append("🔍 Archivos y servicios de inicio detectados en Linux:\n")

    # Archivos de inicio de usuario
    archivos = ["~/.bashrc", "~/.profile", "~/.bash_profile"]
    for archivo in archivos:
        ruta = os.path.expanduser(archivo)
        if os.path.exists(ruta):
            with open(ruta, 'r', errors='ignore') as f:
                lineas = [line.strip() for line in f.readlines() if line.strip() and not line.startswith("#")]
            if lineas:
                resultado.append(f"📄 {archivo}: {len(lineas)} líneas activas\n")
            else:
                resultado.append(f"📄 {archivo}: vacío\n")
        else:
            resultado.append(f"📄 {archivo}: no existe\n")

    # Carpeta de autostart
    autostart_dir = os.path.expanduser("~/.config/autostart")
    if os.path.isdir(autostart_dir):
        archivos = os.listdir(autostart_dir)
        if archivos:
            resultado.append(f"\n🚀 Autostart (~/.config/autostart):\n" + "\n".join(f"  - {a}" for a in archivos))
        else:
            resultado.append("\n🚀 Autostart (~/.config/autostart): sin archivos\n")
    else:
        resultado.append("\n🚀 Autostart (~/.config/autostart): no existe\n")

    # Servicios del sistema
    systemd_dir = "/etc/systemd/system/"
    if os.path.isdir(systemd_dir):
        servicios = [f for f in os.listdir(systemd_dir) if f.endswith(".service")]
        resultado.append(f"\n🛠️ Servicios personalizados en systemd ({len(servicios)} detectados):")
        for s in sorted(servicios)[:10]:  # limitar a 10 primeros
            resultado.append(f"  - {s}")
        if len(servicios) > 10:
            resultado.append("  ... (truncado)")
    else:
        resultado.append("\n🛠️ /etc/systemd/system/ no accesible")

    # Init.d scripts
    initd_dir = "/etc/init.d/"
    if os.path.isdir(initd_dir):
        scripts = os.listdir(initd_dir)
        resultado.append(f"\n🧩 Scripts en /etc/init.d/ ({len(scripts)}):")
        for s in sorted(scripts)[:10]:  # limitar a 10
            resultado.append(f"  - {s}")
        if len(scripts) > 10:
            resultado.append("  ... (truncado)")
