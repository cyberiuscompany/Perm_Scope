# ventanas/about/about.py
from PyQt5.QtWidgets import QMessageBox

def mostrar_about(parent):
    QMessageBox.information(
        parent,
        "Acerca de PermScope",
        "Esta herramienta pertenece a Cyberius Company.\n\n"
        "YouTube: https://www.youtube.com/@CyberiusCompany\n"
        "Discord: https://disboard.org/server/1299310806617292922\n"
        "GitHub: https://github.com/cyberiuscompany"
    )

def mostrar_copyright(parent):
    QMessageBox.information(
        parent,
        "Copyright",
        "© 2025 Cyberius Company. Todos los derechos reservados.\n\n"
        "Esta herramienta está protegida bajo licencia y no puede ser redistribuida sin permiso explícito."
    )

def mostrar_licencia(parent):
    QMessageBox.information(
        parent,
        "Licencia",
        "PermScope es software de código abierto licenciado bajo la licencia MIT.\n\n"
        "Esto significa que puedes usar, copiar, modificar y distribuir este software libremente, "
        "siempre que mantengas el aviso de copyright original y esta nota de licencia.\n\n"
        "Para más información, visita: https://opensource.org/licenses/MIT"
    )
