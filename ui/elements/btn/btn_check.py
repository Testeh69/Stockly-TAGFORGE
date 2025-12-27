from PyQt6.QtWidgets import QPushButton
from PyQt6.QtCore import pyqtSignal, Qt, QSize
from PyQt6.QtGui import QIcon





class BtnCheck(QPushButton):
    toggled_signal = pyqtSignal(bool)

    def __init__(self, parent=None):
        super().__init__(parent)
        
        self.setCheckable(True)
        self.setChecked(True)
        self.clicked.connect(self.on_click)
        self.setIcon(QIcon("assets/selected.svg"))  # chemin vers ton icône
        self.setIconSize(QSize(50, 50))
        self.update_style()
        
    def on_click(self):
        checked = self.isChecked()
        self.toggled_signal.emit(checked)
        self.update_style()

    def update_style(self):
        if self.isChecked():
            self.setStyleSheet(f"background-color: green; color: white;")
        else:
            self.setStyleSheet(f"background-color: none; color: black;")