from PyQt6.QtWidgets import QPushButton
from PyQt6.QtCore import pyqtSignal, QSize
from PyQt6.QtGui import QIcon
from ui.elements.styles.style_btn import StyleGenericBtn


class BtnGen(QPushButton):
    signal = pyqtSignal(bool)

    def __init__(self, parent=None, icon_path:str="assets/bin.svg", size:int=50):
        super().__init__( parent)
        self.clicked.connect(self.on_click)
        self.setIcon(QIcon(f"{icon_path}"))
        self.setIconSize(QSize(size, size))
        self.setStyleSheet(StyleGenericBtn.apply_style_btn())
       
    
    
    def on_click(self):
        self.signal.emit(True)