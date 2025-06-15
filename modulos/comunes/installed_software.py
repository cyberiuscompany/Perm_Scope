import platform
import subprocess
import re
from collections import defaultdict


def ejecutar():
    resultado = []
    sistema = platform.system()

    resultado.append("📦 Software Instalado:\n")

    try:
        if sistema == "Windows":
            resultado.append("🔍 Agrupando software por proveedor...\n")
            cmd = "wmic product get Name, Version, Vendor"
            salida = subprocess.check_output(cmd, shell=True, text=True, stderr=subprocess.DEVNULL)

            lineas = salida.strip().splitlines()
            if len(lineas) < 2:
                resultado.append("❌ No se pudo obtener información del software.")
                return "\n".join(resultado)

            # Detectar columnas dinámicamente
            header = lineas[0]
            index_name = header.find("Name")
            index_vendor = header.find("Vendor")
            index_version = header.find("Version")

            software_por_vendor = defaultdict(list)

            for linea in lineas[1:]:
                if not linea.strip():
                    continue
                nombre = linea[index_name:index_vendor].strip()
                vendor = linea[index_vendor:index_version].strip()
                version = linea[index_version:].strip()

                if nombre:
                    software_por_vendor[vendor].append(f"  - {nombre} (v{version})")

            for vendor, programas in sorted(software_por_vendor.items()):
                if not vendor:
                    vendor = "🔸 (Sin proveedor definido)"
                else:
                    vendor = f"🔸 {vendor}"
                resultado.append(vendor)
                resultado.extend(programas)
                resultado.append("")  # línea en blanco entre vendors

        elif sistema == "Linux":
            resultado.append("🔍 Listando paquetes con dpkg o rpm...\n")
            try:
                salida = subprocess.check_output(
                    "dpkg-query -W -f='${Package}\t${Version}\t${Maintainer}\n'",
                    shell=True, text=True
                )
                software_por_vendor = defaultdict(list)
                for linea in salida.strip().splitlines():
                    parts = linea.strip().split("\t")
                    if len(parts) == 3:
                        nombre, version, maintainer = parts
                        software_por_vendor[maintainer].append(f"  - {nombre} (v{version})")

                for maintainer, paquetes in sorted(software_por_vendor.items()):
                    resultado.append(f"🔸 {maintainer}")
                    resultado.extend(paquetes)
                    resultado.append("")
            except subprocess.CalledProcessError:
                try:
                    salida = subprocess.check_output(
                        "rpm -qa --qf '%{NAME}\t%{VERSION}-%{RELEASE}\t%{VENDOR}\n'",
                        shell=True, text=True
                    )
                    software_por_vendor = defaultdict(list)
                    for linea in salida.strip().splitlines():
                        parts = linea.strip().split("\t")
                        if len(parts) == 3:
                            nombre, version, vendor = parts
                            software_por_vendor[vendor].append(f"  - {nombre} (v{version})")

                    for vendor, paquetes in sorted(software_por_vendor.items()):
                        resultado.append(f"🔸 {vendor}")
                        resultado.extend(paquetes)
                        resultado.append("")
                except subprocess.CalledProcessError:
                    resultado.append("❌ No se pudo detectar gestor de paquetes compatible.")

        else:
            resultado.append("❌ Sistema operativo no compatible.")

    except Exception as e:
        resultado.append(f"[!] Error al listar software instalado: {str(e)}")

    return "\n".join(resultado)
