# modulos/comunes/printer_and_spooler_check.py

import platform
import subprocess
import re

def ejecutar():
    resultado = []
    sistema = platform.system()
    resultado.append("🖨️ Revisión de impresoras y servicio de spooler:\n")

    try:
        if sistema == "Windows":
            # Verificar servicio de spooler
            try:
                estado_spooler = subprocess.check_output("sc query spooler", shell=True, text=True)
                if "RUNNING" in estado_spooler:
                    resultado.append("⚙️ Servicio de Spooler: ACTIVO")
                else:
                    resultado.append("⚠️ Servicio de Spooler: INACTIVO")
            except:
                resultado.append("❌ No se pudo verificar el servicio Spooler.")

            # Listar impresoras
            try:
                impresoras = subprocess.check_output("wmic printer get Name,Default,PortName,PrinterStatus", shell=True, text=True)
                resultado.append("\n🖨️ Impresoras configuradas:\n" + impresoras.strip())
            except:
                resultado.append("❌ No se pudo obtener la lista de impresoras.")

            # Programas relacionados con impresión
            try:
                installed = subprocess.check_output('wmic product get name', shell=True, text=True)
                matches = [line for line in installed.splitlines() if re.search(r"(Canon|Epson|HP|Brother|PDF|Printer)", line, re.I)]
                if matches:
                    resultado.append("\n📦 Programas relacionados con impresoras instalados:")
                    for m in matches:
                        resultado.append(f"  - {m.strip()}")
            except:
                resultado.append("⚠️ No se pudo verificar software de impresoras.")

        elif sistema == "Linux":
            # Verificar si el servicio de CUPS está activo
            try:
                estado_cups = subprocess.check_output("systemctl is-active cups", shell=True, text=True).strip()
                if estado_cups == "active":
                    resultado.append("⚙️ Servicio CUPS (spooler) está ACTIVO")
                else:
                    resultado.append(f"⚠️ Servicio CUPS no está activo: {estado_cups}")
            except:
                resultado.append("❌ No se pudo consultar el estado de CUPS.")

            # Listar impresoras con lpstat
            try:
                impresoras = subprocess.check_output("lpstat -p -d", shell=True, text=True)
                resultado.append("\n🖨️ Impresoras detectadas:\n" + impresoras.strip())
            except:
                resultado.append("⚠️ No se pudieron listar las impresoras con lpstat.")

            # Verificar binarios y archivos conocidos
            try:
                binarios = ["cupsd", "lp", "lpr", "system-config-printer", "hp-setup"]
                encontrados = []
                for b in binarios:
                    if subprocess.call(f"which {b}", shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL) == 0:
                        encontrados.append(b)
                if encontrados:
                    resultado.append("\n📦 Herramientas de impresión disponibles:\n" + "\n".join(f"  - {b}" for b in encontrados))
                else:
                    resultado.append("\n📦 No se detectaron binarios comunes de impresión.")
            except:
                resultado.append("❌ Error al buscar binarios de impresión.")

        else:
            resultado.append("[!] Sistema operativo no soportado.")

    except Exception as e:
        resultado.append(f"[!] Error durante la verificación de impresoras: {str(e)}")

    return "\n".join(resultado)
