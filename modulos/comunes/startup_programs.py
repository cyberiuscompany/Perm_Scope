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
