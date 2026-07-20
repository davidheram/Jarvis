from PyQt6.QtWidgets import QMainWindow, QWidget, QLineEdit, QVBoxLayout, QHBoxLayout, QTextEdit, QPushButton
from PyQt6.QtCore import Qt 
from core.claude import enviar_mensaje
from core.memoria import cargar_historial, guardar_historial

class VentanaJarvis(QMainWindow): 
    def __init__(self):
        super().__init__()
        self.historial = cargar_historial()
        self.iniciar_ui()
        self.mostrar_historial_previo()

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

        boton_limpiar = QPushButton("Nueva conversacion")
        boton_limpiar.clicked.connect(self.limpiar)
        layout_entrada.addWidget(boton_limpiar)

        layout_principal.addLayout(layout_entrada)

    def mostrar_historial_previo(self):
        if self.historial:
            self.area_chat.append("--- Conversacion anterior ---\n")
            for mensaje in self.historial:
                rol = "Tu" if mensaje["role"] == "user" else "Jarvis"
                contenido = mensaje["content"].replace("\n", " ")
                self.area_chat.append(f"{rol}: {contenido}\n")
            self.area_chat.append("--- Nueva sesion ---\n")

    def enviar(self):
        mensaje = self.campo_texto.text().strip()
        if not mensaje:
            return
        
        self.area_chat.append(f"Tu: {mensaje}")
        self.campo_texto.clear()

        self.historial.append({"role":"user", "content":mensaje})
        self.area_chat.append(f"Jarvis:")
        respuesta = enviar_mensaje(self.historial, self.agregar_fragmento)
        self.historial.append({"role": "assistant","content":respuesta})
       
        guardar_historial(self.historial)
        self.area_chat.append("\n")
    

    def agregar_fragmento(self, texto):
        cursor = self.area_chat.textCursor()
        cursor.movePosition(cursor.MoveOperation.End)
        self.area_chat.setTextCursor(cursor)
        self.area_chat.insertPlainText(texto)
        
  

    def limpiar(self): 
        self.historial = []
        guardar_historial(self.historial)
        self.area_chat.clear()
        self.area_chat.append("Nueva conversación iniciada.\n")    



