# modulos/comunes/usb_history_check.py

import platform
import subprocess
import re

def ejecutar():
    resultado = []
    sistema = platform.system()
    resultado.append("🔌 Historial y estado actual de dispositivos USB:\n")

    try:
        if sistema == "Windows":
            # Extraer FriendlyNames del registro
            reg_query = r'reg query HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\Enum\USBSTOR /s /f FriendlyName'
            salida_historial = subprocess.check_output(reg_query, shell=True, text=True, stderr=subprocess.DEVNULL)
            historial = re.findall(r"FriendlyName\s+REG_SZ\s+(.+)", salida_historial)

            # Obtener dispositivos conectados actualmente
            wmic = subprocess.check_output('wmic diskdrive where "InterfaceType=\'USB\'" get Model', shell=True, text=True)
            conectados = re.findall(r"\b(?!Model)(.+)", wmic.strip(), flags=re.MULTILINE)

            if historial:
                resultado.append("📦 Dispositivos USB detectados:\n")
                for item in historial:
                    item_clean = item.strip()
                    estado = "🟢 CONECTADO" if any(item_clean in c for c in conectados) else "⚪ Historial"
                    resultado.append(f"  - {item_clean}  [{estado}]")
            else:
                resultado.append("ℹ️ No se encontraron entradas USB en el registro.")

        elif sistema == "Linux":
            # Obtener dispositivos conectados actualmente
            try:
                lsusb_raw = subprocess.check_output("lsusb", shell=True, text=True)
                conectados = lsusb_raw.strip().splitlines()
            except subprocess.CalledProcessError:
                conectados = []
                resultado.append("[!] Error al ejecutar lsusb.")

            # Obtener historial desde dmesg
            try:
                dmesg = subprocess.check_output("dmesg | grep -i usb | tail -n 50", shell=True, text=True)
                historial = dmesg.strip().splitlines()
            except subprocess.CalledProcessError:
                historial = []
                resultado.append("ℹ️ No se encontraron eventos USB recientes.")

            resultado.append("📦 Dispositivos USB identificados:\n")
            marcas_actuales = [re.search(r'ID\s([\w:]+)\s(.+)', l) for l in conectados]
            nombres_conectados = [m.group(2).strip() for m in marcas_actuales if m]

            for h in historial:
                texto = h.strip()
                estado = "🟢 CONECTADO" if any(nombre in texto for nombre in nombres_conectados) else "⚪ Historial"
                resultado.append(f"  - {texto}  [{estado}]")

        else:
            resultado.append("[!] Sistema operativo no soportado.")

    except Exception as e:
        resultado.append(f"[!] Error durante el análisis USB: {str(e)}")

    return "\n".join(resultado)
