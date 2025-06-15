# modulos/comunes/host_file_entries_check.py

import platform
import os
import re

def ejecutar():
    resultado = []
    sistema = platform.system()
    resultado.append("📄 Análisis de entradas en el archivo 'hosts':\n")

    try:
        # Ruta al archivo hosts según el sistema
        if sistema == "Windows":
            ruta_hosts = r"C:\Windows\System32\drivers\etc\hosts"
        elif sistema == "Linux":
            ruta_hosts = "/etc/hosts"
        else:
            return "[!] Sistema operativo no soportado."

        if not os.path.exists(ruta_hosts):
            return f"[!] No se encontró el archivo: {ruta_hosts}"

        with open(ruta_hosts, "r", encoding="utf-8", errors="ignore") as f:
            lineas = f.readlines()

        entradas = []
        sospechosas = []

        for linea in lineas:
            linea = linea.strip()
            if not linea or linea.startswith("#"):
                continue  # ignorar comentarios y vacías

            entradas.append(linea)

            # Ejemplo de detección: redirección a localhost de dominios populares
            if re.search(r"\b127\.0\.0\.1\b.*(facebook|instagram|twitter|update|microsoft|google)", linea, re.I):
                sospechosas.append(linea)

        if entradas:
            resultado.append("📌 Entradas detectadas:\n" + "\n".join(f"  - {e}" for e in entradas))
        else:
            resultado.append("✅ No se encontraron entradas personalizadas.")

        if sospechosas:
            resultado.append("\n🚨 Entradas potencialmente maliciosas o de bloqueo:\n" + "\n".join(f"  - {s}" for s in sospechosas))
        else:
            resultado.append("\n🟢 No se detectaron redirecciones sospechosas.")

    except Exception as e:
        resultado.append(f"[!] Error al analizar el archivo hosts: {str(e)}")

    return "\n".join(resultado)
