# ventanas/home/home.py
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QListWidget, QLabel, QTabWidget
from PyQt5.QtCore import Qt

class HomeWidget(QWidget):
    def __init__(self, funciones_comunes, funciones_windows, funciones_linux, mostrar_funcion_callback):
        super().__init__()
        self.listas = {}
        self.tabs = QTabWidget()
        self.callback = mostrar_funcion_callback

        for categoria, funciones, nombre_tab in [
            ("comunes", funciones_comunes, "🟦 Comunes"),
            ("windows", funciones_windows, "🟥 Solo Windows"),
            ("linux", funciones_linux, "🟩 Solo Linux")
        ]:
            lista = QListWidget()
            self.listas[categoria] = lista
            for nombre, _ in funciones:
                lista.addItem(nombre)
            lista.currentRowChanged.connect(self.callback)
            tab_widget = QWidget()
            layout = QVBoxLayout()
            layout.addWidget(lista)
            layout.addWidget(QLabel(f"Módulos cargados: {len(funciones)}"))
            tab_widget.setLayout(layout)
            self.tabs.addTab(tab_widget, nombre_tab)

        main_layout = QVBoxLayout()
        main_layout.addWidget(self.tabs)
        self.setLayout(main_layout)

    def obtener_lista_actual(self):
        indice = self.tabs.currentIndex()
        categoria = ["comunes", "windows", "linux"][indice]
        return self.listas[categoria], categoria
