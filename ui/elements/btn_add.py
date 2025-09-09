from PyQt6.QtWidgets import QPushButton
from PyQt6.QtCore import pyqtSignal, QSize
from PyQt6.QtGui import QIcon



class BtnAdd(QPushButton):
    """Bouton personnalisé pour ajouter des éléments dans le tableau."""
    add_signal = pyqtSignal(bool)

    def __init__(self, parent=None):
        super().__init__( parent)
        self.clicked.connect(self.on_click)
        self.setIcon(QIcon("assets/add.svg"))
        self.setIconSize(QSize(50, 50))
    
    
    def on_click(self):
        self.add_signal.emit(True)