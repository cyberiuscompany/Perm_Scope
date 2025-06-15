# modulos/comunes/remote_management_services_check.py

import platform
import subprocess
import shutil

def ejecutar():
    resultado = []
    sistema = platform.system()
    resultado.append("🌐 Servicios de gestión remota detectados:\n")

    try:
        if sistema == "Windows":
            # WinRM
            try:
                salida = subprocess.check_output("winrm enumerate winrm/config/listener", shell=True, text=True, stderr=subprocess.DEVNULL)
                if "Transport" in salida:
                    resultado.append("🟦 WinRM: Activo")
                else:
                    resultado.append("🟦 WinRM: No activo")
            except:
                resultado.append("🟦 WinRM: No disponible")

            # Telnet
            try:
                salida = subprocess.check_output("sc query telnet", shell=True, text=True)
                if "RUNNING" in salida:
                    resultado.append("📞 Telnet: Activo")
                else:
                    resultado.append("📞 Telnet: Instalado pero no activo")
            except:
                resultado.append("📞 Telnet: No instalado")

            # VNC (buscando procesos típicos)
            procesos_vnc = ["vncserver", "winvnc", "tightvnc", "ultravnc", "realvnc"]
            salida = subprocess.getoutput("tasklist")
            vnc_detectados = [p for p in procesos_vnc if p.lower() in salida.lower()]
            if vnc_detectados:
                resultado.append("🖥️ VNC detectado: " + ", ".join(vnc_detectados))
            else:
                resultado.append("🖥️ VNC: No detectado")

        elif sistema == "Linux":
            # SSH
            sshd_status = subprocess.getoutput("systemctl is-active ssh")
            if "active" in sshd_status:
                resultado.append("🔐 SSH: Activo")
            else:
                resultado.append("🔐 SSH: No activo o no instalado")

            # Telnet
            telnet_path = shutil.which("telnetd") or shutil.which("in.telnetd")
            if telnet_path:
                telnet_status = subprocess.getoutput("ps aux | grep -i telnet | grep -v grep")
                if telnet_status:
                    resultado.append("📞 Telnet: Activo")
                else:
                    resultado.append("📞 Telnet: Instalado pero no activo")
            else:
                resultado.append("📞 Telnet: No instalado")

            # VNC (buscando procesos típicos)
            procesos_vnc = ["vncserver", "x11vnc", "tightvncserver", "realvnc", "vino-server"]
            salida = subprocess.getoutput("ps aux")
            vnc_detectados = [p for p in procesos_vnc if p.lower() in salida.lower()]
            if vnc_detectados:
                resultado.append("🖥️ VNC detectado: " + ", ".join(vnc_detectados))
            else:
                resultado.append("🖥️ VNC: No detectado")

        else:
            resultado.append("[!] Sistema no compatible.")

    except Exception as e:
        resultado.append(f"[!] Error al verificar servicios de gestión remota: {str(e)}")

    return "\n".join(resultado)
