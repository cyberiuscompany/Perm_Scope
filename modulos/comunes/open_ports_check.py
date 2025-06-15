# modulos/open_ports_check.py
import platform
import subprocess
import re
from colorama import init, Fore, Style

init(autoreset=True)

# Lista de puertos comunes ampliamente ampliada: servicios web, bases de datos, administración, IoT, etc.
PUERTOS_COMUNES = {
    # Web y proxies
    80, 443, 8080, 8081, 8000, 8443, 8888,

    # Administración remota y escritorio remoto
    22, 23, 3389, 5900, 5985, 5986, 992, 2222, 5800, 3128, 4899,

    # Transferencia de archivos
    20, 21, 69, 115, 989, 990, 2121, 2221, 6621,

    # Correo electrónico
    25, 110, 143, 465, 587, 993, 995,

    # DNS y DHCP
    53, 67, 68, 5353,

    # Bases de datos
    1433, 1434, 1521, 3306, 5432, 27017, 6379, 50000, 50001, 9200, 9300, 27018, 27019,

    # Directorio, RPC y servicios de red
    135, 137, 138, 139, 389, 445, 636, 3268, 3269, 88, 464, 123, 42,

    # VPN y tunelización
    1723, 1194, 500, 1701, 4500, 1197, 1198, 51820, 51821,

    # IoT y dispositivos
    554, 49152, 49153, 49154, 49155, 49156, 49157, 8200, 49158,

    # Varios / Herramientas / Monitorización
    873, 9090, 10000, 161, 162, 3000, 5601, 15672, 61616, 1883, 8883, 9092, 6667
}

# Opcional: puertos considerados especialmente sensibles
PUERTOS_PELIGROSOS = {23, 445, 3389, 21, 69, 2049, 111, 5800, 5900, 20, 137, 138, 139, 512, 513, 514, 1111}

def resaltar_puertos(salida):
    resaltado = []
    comunes_detectados = set()
    peligrosos = set()

    for linea in salida.strip().splitlines():
        match = re.search(r":(\d+)", linea)
        if match:
            puerto = int(match.group(1))
            if puerto in PUERTOS_COMUNES:
                comunes_detectados.add(puerto)
                if puerto in PUERTOS_PELIGROSOS:
                    linea_coloreada = f"{Fore.YELLOW}[⚠️] {linea}{Style.RESET_ALL}"
                    peligrosos.add(puerto)
                else:
                    linea_coloreada = f"{Fore.GREEN}{linea}{Style.RESET_ALL}"
            else:
                linea_coloreada = linea
        else:
            linea_coloreada = linea
        resaltado.append(linea_coloreada)

    return "\n".join(resaltado), comunes_detectados, peligrosos

def ejecutar():
    resultado = []
    sistema = platform.system()
    comunes_encontrados = set()
    peligrosos_encontrados = set()

    resultado.append("🔌 Revisión de puertos abiertos en el sistema:\n")

    try:
        if sistema == "Windows":
            resultado.append("Usando: netstat -ano\n")
            salida = subprocess.check_output("netstat -ano", shell=True, text=True)
            resaltado, comunes_encontrados, peligrosos_encontrados = resaltar_puertos(salida)
            resultado.append(resaltado)

        elif sistema == "Linux":
            try:
                resultado.append("Usando: ss -tulnp\n")
                salida = subprocess.check_output("ss -tulnp", shell=True, text=True)
                resaltado, comunes_encontrados, peligrosos_encontrados = resaltar_puertos(salida)
                resultado.append(resaltado)
            except subprocess.CalledProcessError:
                resultado.append("Fallo 'ss', intentando con: netstat -tulnp\n")
                salida = subprocess.check_output("netstat -tulnp", shell=True, text=True)
                resaltado, comunes_encontrados, peligrosos_encontrados = resaltar_puertos(salida)
                resultado.append(resaltado)

        else:
            resultado.append("Sistema operativo no soportado para este módulo.")
            return "\n".join(resultado)

        if comunes_encontrados:
            resultado.append(f"\n✅ Puertos comunes abiertos: {Fore.GREEN}{', '.join(map(str, sorted(comunes_encontrados)))}{Style.RESET_ALL}")
        else:
            resultado.append("\n⚠️ No se detectaron puertos comunes abiertos.")

        if peligrosos_encontrados:
            resultado.append(f"{Fore.YELLOW}\n⚠️ Puertos potencialmente peligrosos detectados: {', '.join(map(str, sorted(peligrosos_encontrados)))}{Style.RESET_ALL}")

    except Exception as e:
        resultado.append(f"[!] Error al obtener puertos abiertos: {str(e)}")

    return "\n".join(resultado) + "\n"
