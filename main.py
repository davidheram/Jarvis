import sys 
from PyQt6.QtWidgets import QApplication
from ui.ventana import VentanaJarvis


if __name__ == "__main__":
    app = QApplication(sys.argv)
    ventana = VentanaJarvis()
    ventana.show()
    sys.exit(app.exec())
