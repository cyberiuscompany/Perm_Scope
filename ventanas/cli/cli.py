# ventanas/cli/cli.py
import platform
from PyQt5.QtWidgets import QWidget, QPlainTextEdit, QLineEdit, QVBoxLayout, QHBoxLayout, QPushButton
from PyQt5.QtCore import QProcess

class TerminalWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.layout = QVBoxLayout()

        self.terminal1 = self.crear_terminal()
        self.terminal2 = self.crear_terminal()

        self.clear_btn1 = QPushButton("🧹 Clear 1")
        self.clear_btn1.clicked.connect(lambda: self.terminal1['output'].clear())
        self.clear_btn2 = QPushButton("🧹 Clear 2")
        self.clear_btn2.clicked.connect(lambda: self.terminal2['output'].clear())

        btn_layout = QHBoxLayout()
        btn_layout.addWidget(self.clear_btn1)
        btn_layout.addWidget(self.clear_btn2)

        self.layout.addLayout(btn_layout)

        term_layout = QHBoxLayout()
        term_layout.addLayout(self.terminal1['layout'])
        term_layout.addLayout(self.terminal2['layout'])

        self.layout.addLayout(term_layout)
        self.setLayout(self.layout)

    def crear_terminal(self):
        output = QPlainTextEdit()
        output.setReadOnly(True)

        input_line = QLineEdit()
        process = QProcess()

        shell = "cmd" if platform.system() == "Windows" else "/bin/bash"
        process.setProgram(shell)
        process.setProcessChannelMode(QProcess.MergedChannels)
        process.readyReadStandardOutput.connect(lambda: output.appendPlainText(process.readAllStandardOutput().data().decode(errors="ignore")))

        input_line.returnPressed.connect(lambda: self.enviar_comando(process, input_line))

        layout = QVBoxLayout()
        layout.addWidget(output)
        layout.addWidget(input_line)

        return {"output": output, "input": input_line, "process": process, "layout": layout}

    def iniciar(self):
        try:
            if self.terminal1['process'].state() != QProcess.Running:
                self.terminal1['process'].start()
            if self.terminal2['process'].state() != QProcess.Running:
                self.terminal2['process'].start()
        except Exception as e:
            self.terminal1['output'].appendPlainText(f"[ERROR] {str(e)}")

    def enviar_comando(self, process, input_line):
        try:
            if process and process.state() == QProcess.Running:
                comando = input_line.text() + "\n"
                process.write(comando.encode())
                input_line.clear()
        except Exception as e:
            print(f"Error enviando comando: {e}")

    def ocultar(self):
        self.hide()
        self.terminal1['input'].clear()
        self.terminal1['output'].clear()
        self.terminal2['input'].clear()
        self.terminal2['output'].clear()
