# modulos/scheduled_tasks.py
import platform
import subprocess


def ejecutar():
    resultado = []
    sistema = platform.system()

    if sistema == "Windows":
        resultado.append("📅 Tareas programadas en Windows:\n")
        try:
            salida = subprocess.check_output("schtasks /query /fo LIST /v", shell=True, text=True, stderr=subprocess.DEVNULL)
            tareas = salida.split("\n\n")
            for tarea in tareas:
                if "TaskName:" in tarea:
                    # Añade un salto de línea entre HostName y TaskName para claridad visual
                    tarea = tarea.replace("TaskName:", "\nTaskName:")
                    resultado.append(tarea.strip())
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
