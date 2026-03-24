import sys
from PyQt6.QtWidgets import QApplication
from ui.mainWindow import StockTagForgeMainWindow

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = StockTagForgeMainWindow()
    window.show()
    sys.exit(app.exec())