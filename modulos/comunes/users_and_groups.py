# modulos/comunes/users_and_groups.py

import platform
import subprocess
import os

def ejecutar():
    resultado = []
    sistema = platform.system()

    resultado.append("👥 Usuarios, grupos locales y administradores:\n")

    try:
        if sistema == "Windows":
            # Usuarios
            usuarios = subprocess.check_output("net user", shell=True, text=True)
            resultado.append("👤 Usuarios (net user):\n" + usuarios)

            # Grupos
            grupos = subprocess.check_output("net localgroup", shell=True, text=True)
            resultado.append("👥 Grupos (net localgroup):\n" + grupos)

            # Administradores
            admins = subprocess.check_output("net localgroup Administrators", shell=True, text=True)
            resultado.append("🛡️ Usuarios con privilegios de administrador (Administrators):\n" + admins)

        elif sistema == "Linux":
            # Usuarios desde /etc/passwd
            if os.path.exists("/etc/passwd"):
                resultado.append("👤 Usuarios (/etc/passwd):")
                with open("/etc/passwd", "r") as f:
                    for linea in f:
                        if not linea.startswith("#"):
                            campos = linea.strip().split(":")
                            if int(campos[2]) >= 1000 and campos[0] != "nobody":
                                resultado.append(f"  - {campos[0]} (UID: {campos[2]}, Shell: {campos[6]})")

            # Grupos desde /etc/group
            if os.path.exists("/etc/group"):
                resultado.append("\n👥 Grupos (/etc/group):")
                with open("/etc/group", "r") as f:
                    for linea in f:
                        if not linea.startswith("#"):
                            campos = linea.strip().split(":")
                            resultado.append(f"  - {campos[0]} (GID: {campos[2]})")

            # Administradores: miembros del grupo sudo
            try:
                sudoers = subprocess.check_output("getent group sudo", shell=True, text=True)
                resultado.append("\n🛡️ Usuarios con privilegios de administrador (grupo sudo):\n" + sudoers)
            except subprocess.CalledProcessError:
                resultado.append("\n[!] No se pudo obtener el grupo sudo.")

        else:
            resultado.append("[!] Sistema operativo no soportado.")

    except Exception as e:
        resultado.append(f"[!] Error al obtener usuarios y grupos: {str(e)}")

    return "\n".join(resultado)
