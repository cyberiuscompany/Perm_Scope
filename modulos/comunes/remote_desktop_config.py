# modulos/remote_desktop_config.py
import platform
import subprocess
import os


def ejecutar():
    resultado = []
    sistema = platform.system()

    resultado.append("🖥️ Configuración de Escritorio Remoto:\n")

    try:
        if sistema == "Windows":
            resultado.append("🔍 Comprobando RDP con: reg query y servicios...")

            try:
                # Verificar si RDP está habilitado en el registro
                reg_cmd = 'reg query "HKLM\\System\\CurrentControlSet\\Control\\Terminal Server" /v fDenyTSConnections'
                reg_out = subprocess.check_output(reg_cmd, shell=True, text=True)
                if '0x0' in reg_out:
                    resultado.append("✅ RDP está habilitado en el sistema (fDenyTSConnections=0)")
                elif '0x1' in reg_out:
                    resultado.append("❌ RDP está deshabilitado (fDenyTSConnections=1)")
                else:
                    resultado.append("⚠️ No se pudo determinar claramente el estado de RDP.")
            except Exception as e:
                resultado.append(f"[!] Error al consultar el registro: {e}")

            # Verificar servicio
            try:
                status = subprocess.check_output("sc query TermService", shell=True, text=True)
                resultado.append("\n🛠️ Servicio de Terminal Services:")
                resultado.append(status.strip())
            except Exception as e:
                resultado.append(f"[!] Error al comprobar el servicio TermService: {e}")

            # Comprobación de redirección del portapapeles
            resultado.append("\n📋 Redirección del portapapeles en sesiones RDP:")
            try:
                cmd = 'reg query "HKLM\\Software\\Policies\\Microsoft\\Windows NT\\Terminal Services" /v fDisableClip'
                salida = subprocess.check_output(cmd, shell=True, text=True)
                if '0x0' in salida:
                    resultado.append("✅ La redirección del portapapeles RDP está habilitada (fDisableClip=0)")
                elif '0x1' in salida:
                    resultado.append("❌ La redirección del portapapeles RDP está deshabilitada (fDisableClip=1)")
                else:
                    resultado.append("⚠️ No se pudo interpretar claramente el valor de fDisableClip")
            except subprocess.CalledProcessError:
                resultado.append("⚠️ No se encontró configuración explícita en el registro (podría estar habilitado por defecto)")

        elif sistema == "Linux":
            resultado.append("🔍 Buscando servicios RDP en Linux como xrdp, vino o VNC...")
            servicios = ["xrdp", "vino-server", "vncserver"]
            encontrados = []

            for servicio in servicios:
                try:
                    status = subprocess.check_output(f"systemctl is-active {servicio}", shell=True, text=True).strip()
                    encontrados.append(f"✅ {servicio} está activo.")
                except subprocess.CalledProcessError:
                    encontrados.append(f"❌ {servicio} no está activo o no está instalado.")

            resultado.extend(encontrados)

            # Comprobación de xrdp-chansrv
            resultado.append("\n📋 Redirección del portapapeles en xrdp:")
            try:
                chansrv_status = subprocess.check_output("ps aux | grep xrdp-chansrv | grep -v grep", shell=True, text=True).strip()
                if chansrv_status:
                    resultado.append("✅ xrdp-chansrv en ejecución: Redirección de portapapeles habilitada.")
                else:
                    resultado.append("❌ xrdp-chansrv no está en ejecución.")
            except subprocess.CalledProcessError:
                resultado.append("❌ xrdp-chansrv no está corriendo.")

        else:
            resultado.append("Sistema operativo no soportado para este módulo.")

    except Exception as e:
        resultado.append(f"[!] Error general al comprobar Escritorio Remoto: {str(e)}")

    return "\n".join(resultado)
