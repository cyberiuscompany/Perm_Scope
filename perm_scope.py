import sys
import platform
import subprocess
import importlib
import traceback
import os
import getpass
import argparse
from datetime import datetime
from PyQt5.QtGui import QIcon
from colorama import init, Fore, Style
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QTextEdit, QMessageBox, QSplitter,
    QAction, QMenuBar, QLabel, QVBoxLayout, QWidget, QPushButton, QHBoxLayout as QHBox
)
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt, QTimer

from ventanas.cli.cli import TerminalWidget
from ventanas.about.about import mostrar_about, mostrar_copyright, mostrar_licencia
from ventanas.home.home import HomeWidget

init(autoreset=True)  # Inicializa colorama para colores en consola

FUNCIONES_COMUNES = []
FUNCIONES_WINDOWS = []
FUNCIONES_LINUX = []
ESTADOS_CARGA = {}

modo_oscuro = False

def mostrar_banner():
    banner_path = os.path.join(os.path.dirname(__file__), "banner.txt")
    if os.path.isfile(banner_path):
        with open(banner_path, "r", encoding="utf-8") as f:
            print(f.read())

def cargar_funciones():
    base_dir = os.path.join(os.path.dirname(__file__), 'modulos')
    for categoria, lista_funciones in [
        ('comunes', FUNCIONES_COMUNES),
        ('windows', FUNCIONES_WINDOWS),
        ('linux', FUNCIONES_LINUX)
    ]:
        path_dir = os.path.join(base_dir, categoria)
        if not os.path.isdir(path_dir):
            continue
        modulos = [f for f in os.listdir(path_dir) if f.endswith(".py") and not f.startswith("__")]
        modulos.sort(key=lambda x: (0 if x == "whoami_all.py" else 1, x))
        for fname in modulos:
            nombre = fname.replace(".py", "")
            path = f"modulos.{categoria}.{nombre}"
            texto_lista = f"{len(lista_funciones)+1}. {nombre.replace('_', ' ').title()} [ ]"
            lista_funciones.append((texto_lista, path))
            ESTADOS_CARGA[path] = False

def ejecutar_modulo(modulo_path):
    try:
        nombre_modulo = modulo_path.split('.')[-1]
        print(Fore.CYAN + f"\n[>] Ejecutando módulo: {nombre_modulo}")
        modulo = importlib.import_module(modulo_path)
        if hasattr(modulo, "ejecutar"):
            salida = modulo.ejecutar()
            print(salida)
            print(Fore.GREEN + f"[✓] Finalizado correctamente: {nombre_modulo}\n")
        else:
            print(Fore.YELLOW + f"[!] El módulo {nombre_modulo} no tiene función 'ejecutar'\n")
    except Exception as e:
        print(Fore.RED + f"[✗] Error al ejecutar {modulo_path}:\n{str(e)}\n")
        print(traceback.format_exc())

def modo_consola(args):
    cargar_funciones()
    if args.listar:
        print(Fore.BLUE + "\n🟦 Comunes:")
        for nombre, _ in FUNCIONES_COMUNES:
            print("   ", nombre.replace("[ ]", ""))
        print(Fore.RED + "\n🟥 Solo Windows:")
        for nombre, _ in FUNCIONES_WINDOWS:
            print("   ", nombre.replace("[ ]", ""))
        print(Fore.GREEN + "\n🟩 Solo Linux:")
        for nombre, _ in FUNCIONES_LINUX:
            print("   ", nombre.replace("[ ]", ""))
        return

    if args.modulo:
        for lista in [FUNCIONES_COMUNES, FUNCIONES_WINDOWS, FUNCIONES_LINUX]:
            for nombre, path in lista:
                if args.modulo == path.split('.')[-1]:
                    ejecutar_modulo(path)
                    return
        print(Fore.RED + f"[!] Módulo '{args.modulo}' no encontrado.")
        return

    if args.modulos:
        nombres = [x.strip() for x in args.modulos.split(',')]
        encontrados = 0
        for nombre in nombres:
            for lista in [FUNCIONES_COMUNES, FUNCIONES_WINDOWS, FUNCIONES_LINUX]:
                for mod_nombre, path in lista:
                    if nombre == path.split('.')[-1]:
                        ejecutar_modulo(path)
                        encontrados += 1
        if encontrados == 0:
            print(Fore.RED + "[!] No se encontró ningún módulo especificado.")

    if args.tipo:
        tipo = args.tipo.lower()
        if tipo == "comunes":
            for _, path in FUNCIONES_COMUNES:
                ejecutar_modulo(path)
        elif tipo == "windows":
            for _, path in FUNCIONES_WINDOWS:
                ejecutar_modulo(path)
        elif tipo == "linux":
            for _, path in FUNCIONES_LINUX:
                ejecutar_modulo(path)
        else:
            print(Fore.RED + "[!] Tipo inválido. Usa: comunes, windows, linux.")

def mostrar_ayuda():
    print(Fore.YELLOW + """
PermScope - Análisis y recolección local
----------------------------------------

USO:
    python perm_scope.py --modo gui
    python perm_scope.py --modo consola + [opciones]

COMANDOS MAS POTENTES:
    python perm_scope.py --modo consola --tipo comunes
    python perm_scope.py --modo consola --tipo windows
    python perm_scope.py --modo consola --tipo linux

OPCIONES CON --modo consola:

    --listar
        Muestra todos los módulos disponibles:
        * (A la hora de escribir el nombre recuerda la "_" en los espacios)
        🟦 Comunes (Linux & Windows) (Visión General) 
        🟥 Solo Windows (Ofensivos)
        🟩 Solo Linux (Ofensives)

    --modulo NOMBRE
        Ejecuta un módulo exacto (sin .py)
        Ej: python perm_scope.py --modo consola --modulo whoami_all

    --modulos N1,N2,... (Fijate que los espacio son "_" en cada modulo)
        Ejecuta varios módulos
        Ej: python perm_scope.py --modo consola --modulos whoami_all,users_logged

    --tipo comunes|windows|linux
        Ejecuta todos los módulos de un tipo

    --help
        Muestra esta ayuda

""")

class ZoomableTextEdit(QTextEdit):
    def __init__(self):
        super().__init__()
        self.default_size = 10
        self.setFont(QFont("Courier New", self.default_size))

    def wheelEvent(self, event):
        if event.modifiers() == Qt.ControlModifier:
            if event.angleDelta().y() > 0:
                self.zoomIn(1)
            else:
                self.zoomOut(1)
        else:
            super().wheelEvent(event)

class PermScope(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("PermScope - Panel de utilidades")
        self.setGeometry(100, 100, 1000, 600)
        self.setWindowIcon(QIcon(os.path.join(os.path.dirname(__file__), "Icono.ico")))
        self.init_ui()

    def init_ui(self):
        menu_bar = QMenuBar(self)
        self.setMenuBar(menu_bar)

        home_action = QAction("🏠 Home", self)
        home_action.triggered.connect(self.volver_a_home)
        menu_bar.addAction(home_action)

        cli_action = QAction("💻 CLI", self)
        cli_action.triggered.connect(self.mostrar_terminal_incrustada)
        menu_bar.addAction(cli_action)

        ayuda_menu = menu_bar.addMenu("Ayuda")
        ayuda_menu.addAction("Acerca de", lambda: mostrar_about(self))
        ayuda_menu.addAction("Copyright", lambda: mostrar_copyright(self))
        ayuda_menu.addAction("Licencia", lambda: mostrar_licencia(self))

        self.info_bar = QLabel()
        self.boton_modo = QPushButton("Modo oscuro")
        self.boton_modo.clicked.connect(self.toggle_modo_oscuro)
        self.actualizar_info_bar()

        barra_extra = QWidget()
        barra_layout = QHBox()
        barra_layout.setContentsMargins(0, 0, 0, 0)
        barra_layout.setSpacing(10)
        barra_layout.addWidget(self.info_bar)
        barra_layout.addWidget(self.boton_modo)
        barra_extra.setLayout(barra_layout)
        menu_bar.setCornerWidget(barra_extra, Qt.TopRightCorner)

        timer = QTimer(self)
        timer.timeout.connect(self.actualizar_info_bar)
        timer.start(1000)

        self.terminal_widget = TerminalWidget()
        self.terminal_widget.hide()

        self.home_widget = HomeWidget(FUNCIONES_COMUNES, FUNCIONES_WINDOWS, FUNCIONES_LINUX, self.mostrar_funcion)
        self.texto_salida = ZoomableTextEdit()
        self.texto_salida.setReadOnly(True)

        self.layout_principal = QSplitter(Qt.Horizontal)
        self.layout_principal.addWidget(self.home_widget)
        self.layout_principal.addWidget(self.texto_salida)
        self.layout_principal.setStretchFactor(0, 1)
        self.layout_principal.setStretchFactor(1, 4)

        self.contenedor = QWidget()
        self.layout_total = QVBoxLayout()
        self.layout_total.addWidget(self.layout_principal)
        self.layout_total.addWidget(self.terminal_widget)
        self.contenedor.setLayout(self.layout_total)
        self.setCentralWidget(self.contenedor)

    def actualizar_info_bar(self):
        user = getpass.getuser()
        now = datetime.now().strftime("%H:%M:%S")
        tipo_usuario = self.obtener_tipo_usuario()
        self.info_bar.setText(f" 🕒 {now}   👤 {user} ({tipo_usuario})  ")

    def toggle_modo_oscuro(self):
        global modo_oscuro
        modo_oscuro = not modo_oscuro
        if modo_oscuro:
            self.setStyleSheet("QWidget { background-color: #121212; color: white; }")
            self.boton_modo.setText("Modo claro")
        else:
            self.setStyleSheet("")
            self.boton_modo.setText("Modo oscuro")

    def obtener_tipo_usuario(self):
        if platform.system() == "Windows":
            try:
                salida = subprocess.check_output("whoami", shell=True, text=True).strip()
                if "\\" in salida:
                    dominio = salida.split("\\")[0].lower()
                    if dominio not in [platform.node().lower(), "localhost"]:
                        return "AD"
                return "Local"
            except:
                return "Desconocido"
        else:
            return "Local"

    def mostrar_funcion(self, indice):
        try:
            lista_widget, categoria = self.home_widget.obtener_lista_actual()
            funciones = {
                "comunes": FUNCIONES_COMUNES,
                "windows": FUNCIONES_WINDOWS,
                "linux": FUNCIONES_LINUX
            }[categoria]

            if 0 <= indice < len(funciones):
                nombre, modulo_path = funciones[indice]
                modulo = importlib.import_module(modulo_path)
                if hasattr(modulo, "ejecutar"):
                    salida = modulo.ejecutar()
                    self.texto_salida.setPlainText(salida)
                    ESTADOS_CARGA[modulo_path] = True
                    lista_widget.item(indice).setText(nombre.replace("[ ]", "[✓]"))
                else:
                    self.texto_salida.setPlainText("El módulo no tiene función 'ejecutar'.")
        except Exception as e:
            self.texto_salida.setPlainText(f"Error al mostrar función: {str(e)}")
            print(f"Error: {str(e)}\n{traceback.format_exc()}")

    def mostrar_terminal_incrustada(self):
        self.layout_principal.hide()
        self.terminal_widget.show()
        self.terminal_widget.iniciar()

    def volver_a_home(self):
        self.terminal_widget.hide()
        self.layout_principal.show()

def main():
    parser = argparse.ArgumentParser(add_help=False)
    parser.add_argument("--modo", choices=["gui", "consola"])
    parser.add_argument("--listar", action="store_true")
    parser.add_argument("--modulo")
    parser.add_argument("--modulos")
    parser.add_argument("--tipo")
    parser.add_argument("--help", action="store_true")

    args = parser.parse_args()

    if args.help or args.modo is None:
        mostrar_banner()
        mostrar_ayuda()
        
        # NUEVO: mostrar resumen de módulos al ejecutar sin parámetros
        cargar_funciones()
        print(Fore.CYAN + "\n📦 Módulos disponibles detectados:\n")
        print(Fore.BLUE + f"🟦 Comunes (Revisión General):        {len(FUNCIONES_COMUNES)} módulos")
        print(Fore.RED + f"🟥 Solo Windows (Ofensivos):   {len(FUNCIONES_WINDOWS)} módulos")
        print(Fore.GREEN + f"🟩 Solo Linux (Ofensivos):     {len(FUNCIONES_LINUX)} módulos")

        print(Fore.YELLOW + "\nℹ️  Usa '--listar' para ver los nombres completos.\n")
        return

    if args.modo == "gui":
        cargar_funciones()
        app = QApplication(sys.argv)
        ventana = PermScope()
        ventana.show()
        sys.exit(app.exec_())

    elif args.modo == "consola":
        mostrar_banner()
        modo_consola(args)


if __name__ == "__main__":
    main()
