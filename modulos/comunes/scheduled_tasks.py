import platform
import subprocess
from collections import defaultdict


def ejecutar():
    resultado = []
    sistema = platform.system()

    if sistema == "Windows":
        resumen_por_usuario = defaultdict(int)

        try:
            salida = subprocess.check_output("schtasks /query /fo LIST /v", shell=True, text=True, stderr=subprocess.DEVNULL)
            tareas = salida.split("\n\n")
            total_tareas = 0

            for tarea in tareas:
                if "TaskName:" in tarea:
                    lineas = tarea.strip().splitlines()
                    info = {}
                    for linea in lineas:
                        if ":" in linea:
                            clave, valor = linea.split(":", 1)
                            clave = clave.strip()
                            valor = valor.strip()
                            if "N/A" not in valor:
                                info[clave] = valor

                    if "TaskName" in info:
                        raw_user = info.get("Run As User", "Desconocido")
                        usuario = raw_user.split("\\")[-1] if "\\" in raw_user else raw_user
                        resumen_por_usuario[usuario] += 1
                        total_tareas += 1

            resultado.append(f"📋 Total de tareas programadas encontradas: {total_tareas}\n")
            resultado.append("📊 Resumen por usuario que ejecuta tareas:\n")
            for usuario, cantidad in resumen_por_usuario.items():
                resultado.append(f"👤 {usuario}: {cantidad} tarea(s)")

        except Exception as e:
            resultado.append(f"[!] Error al obtener tareas programadas: {str(e)}")

    elif sistema == "Linux":
        resultado.append("📅 Tareas programadas encontradas en Linux:\n")

        # Crontab del usuario actual
        try:
            crontab_user = subprocess.check_output("crontab -l", shell=True, text=True)
            lineas = [l for l in crontab_user.splitlines() if l.strip() and not l.strip().startswith("#")]
            if lineas:
                resultado.append("🔸 Crontab del usuario actual:")
                resultado.extend(f"  - {l}" for l in lineas)
            else:
                resultado.append("🔸 Crontab del usuario actual: vacío.")
        except subprocess.CalledProcessError:
            resultado.append("🔸 Crontab del usuario actual: no definido.")

        # /etc/crontab
        try:
            cron_sys = subprocess.check_output("cat /etc/crontab", shell=True, text=True)
            lineas = [l for l in cron_sys.splitlines() if l.strip() and not l.strip().startswith("#") and not l.startswith("SHELL=")]
            if lineas:
                resultado.append("\n🔸 /etc/crontab:")
                resultado.extend(f"  - {l}" for l in lineas)
            else:
                resultado.append("\n🔸 /etc/crontab: sin tareas activas.")
        except Exception as e:
            resultado.append(f"[!] Error al leer /etc/crontab: {str(e)}")

        # Archivos en /etc/cron.d
        try:
            archivos = subprocess.check_output("ls /etc/cron.d", shell=True, text=True).splitlines()
            if archivos:
                resultado.append("\n🗂️ Archivos en /etc/cron.d:")
                for archivo in archivos:
                    ruta = f"/etc/cron.d/{archivo}"
                    try:
                        with open(ruta, 'r') as f:
                            lineas = [l for l in f if l.strip() and not l.strip().startswith("#")]
                            if lineas:
                                resultado.append(f"  📄 {archivo}:")
                                resultado.extend(f"    - {l.strip()}" for l in lineas)
                    except:
                        resultado.append(f"  📄 {archivo}: error al leer")
            else:
                resultado.append("\n🗂️ /etc/cron.d: sin archivos.")
        except Exception as e:
            resultado.append(f"[!] Error al listar /etc/cron.d: {str(e)}")

    else:
        resultado.append("❌ Sistema operativo no soportado para este módulo.")

    return "\n".join(resultado)
