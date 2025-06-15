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
        resultado.append("📅 Tareas programadas en Linux (crontabs):\n")
        try:
            crontab_user = subprocess.check_output("crontab -l", shell=True, text=True)
            resultado.append("🔸 Crontab del usuario actual:\n" + crontab_user)
        except subprocess.CalledProcessError:
            resultado.append("[i] No hay crontab definido para el usuario actual.")

        try:
            cron_sys = subprocess.check_output("cat /etc/crontab", shell=True, text=True)
            resultado.append("\n🔸 /etc/crontab:\n" + cron_sys)
        except Exception as e:
            resultado.append(f"[!] Error al leer /etc/crontab: {str(e)}")

        try:
            resultado.append("\n🔸 Archivos en /etc/cron.d:\n")
            cron_d = subprocess.check_output("ls -l /etc/cron.d", shell=True, text=True)
            resultado.append(cron_d)
        except Exception as e:
            resultado.append(f"[!] Error al listar /etc/cron.d: {str(e)}")

    else:
        resultado.append("Sistema operativo no soportado para este módulo.")

    return "\n".join(resultado)
