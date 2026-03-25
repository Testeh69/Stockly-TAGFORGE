from PyQt6.QtWidgets import QToolButton
from PyQt6.QtCore import pyqtSignal, Qt, QSize
from PyQt6.QtGui import QIcon





class BtnCheck(QToolButton):
    toggled_signal = pyqtSignal(bool)

    def __init__(self, parent=None):
        super().__init__(parent)
        
        self.setCheckable(True)
        self.setChecked(True)
        self.clicked.connect(self.on_click)
        self.setIcon(QIcon("assets/selected.svg"))  # chemin vers ton icône
        self.setIconSize(QSize(50, 50))
        self.update_style()
        self.setText("VALIDER")
        
        
    def on_click(self):
        checked = self.isChecked()
        self.toggled_signal.emit(checked)
        self.update_style()

    def update_style(self):
        self.setToolButtonStyle(Qt.ToolButtonStyle.ToolButtonTextUnderIcon)
        if self.isChecked():
            self.setStyleSheet(f"background-color: green; color: white; border-top-right-radius: 5px;")
        else:
            self.setStyleSheet(f"background-color: none; color: black; border-top-right-radius: 5px;")