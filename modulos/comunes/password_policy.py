import platform
import subprocess


def ejecutar():
    resultado = []
    sistema = platform.system()

    resultado.append("🔐 Política de contraseñas del sistema:\n")

    try:
        if sistema == "Windows":
            resultado.append("Usando: net accounts\n")
            salida = subprocess.check_output("net accounts", shell=True, text=True)
            resultado.append(salida)

            resultado.append("\n⚠️ Política local avanzada (secpol.msc) no disponible vía CLI.")

        elif sistema == "Linux":
            resultado.append("Usando: /etc/login.defs y chage\n")

            # Extraer líneas clave de login.defs
            try:
                with open("/etc/login.defs", "r") as f:
                    lineas_utiles = []
                    for linea in f:
                        if linea.startswith("PASS_"):
                            lineas_utiles.append(linea.strip())
                if lineas_utiles:
                    resultado.append("\n[Parámetros de /etc/login.defs]")
                    resultado.extend(f"  - {l}" for l in lineas_utiles)
                else:
                    resultado.append("[/etc/login.defs] No se encontraron parámetros PASS_*")
            except Exception as e:
                resultado.append(f"No se pudo leer /etc/login.defs: {e}")

            # chage para usuario actual
            resultado.append("\n[Política por usuario actual - chage -l]")
            try:
                salida = subprocess.check_output("chage -l $(whoami)", shell=True, text=True)
                resultado.append(salida.strip())
            except:
                resultado.append("No se pudo ejecutar chage para el usuario actual.")

        else:
            resultado.append("❌ Sistema operativo no soportado para este módulo.")

    except Exception as e:
        resultado.append(f"[!] Error al obtener política de contraseñas: {str(e)}")

    return "\n".join(resultado)
