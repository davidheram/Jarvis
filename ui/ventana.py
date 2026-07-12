from PyQt6.QtWidgets import QMainWindow, QWidget, QLineEdit, QVBoxLayout, QHBoxLayout, QTextEdit, QPushButton
from PyQt6.QtCore import Qt 
from core.claude import enviar_mensaje

class VentanaJarvis(QMainWindow): 
    def __init__(self):
        super().__init__()
        self.historial =[]
        self.iniciar_ui()

    def iniciar_ui(self):
        self.setWindowTitle("Jarvis")
        self.setMinimumSize(800, 600)

        widget_central = QWidget()
        self.setCentralWidget(widget_central)
        layout_principal = QVBoxLayout(widget_central)

        self.area_chat = QTextEdit()
        self.area_chat.setReadOnly(True)
        layout_principal.addWidget(self.area_chat)

        layout_entrada = QHBoxLayout()
        self.campo_texto = QLineEdit()
        self.campo_texto.setPlaceholderText("Escribe tu mensaje aquí...")
        self.campo_texto.returnPressed.connect(self.enviar)
        layout_entrada.addWidget(self.campo_texto)

        self.boton_enviar = QPushButton("Enviar")
        self.boton_enviar.clicked.connect(self.enviar)
        layout_entrada.addWidget(self.boton_enviar)

        layout_principal.addLayout(layout_entrada)

    def enviar(self):
        mensaje = self.campo_texto.text().strip()
        if not mensaje:
            return
        
        self.area_chat.append(f"Tu: {mensaje}")
        self.campo_texto.clear()

        self.historial.append({"role":"user", "content":mensaje})
        respuesta = enviar_mensaje(self.historial)
        self.historial.append({"role": "assistant","content":respuesta})

        self.area_chat.append(f"Jarvis: {respuesta}\n")


