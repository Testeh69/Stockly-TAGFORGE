from PyQt6.QtWidgets import QToolButton 
from PyQt6.QtCore import pyqtSignal, QSize,Qt
from PyQt6.QtGui import QIcon
from ui.elements.styles.style_btn import StyleGenericBtn


class BtnGen(QToolButton):
    signal = pyqtSignal(bool)

    def __init__(self, parent=None, text:str=None, icon_path:str="assets/bin.svg", size:int=50, style:str = None):
        super().__init__( parent)
        self.clicked.connect(self.on_click)
        self.setIcon(QIcon(f"{icon_path}"))
        self.setIconSize(QSize(size, size))
        self.setText(text if text else "")
        self.setStyleSheet(style if style else StyleGenericBtn.apply_style_btn())
        self.setToolButtonStyle(Qt.ToolButtonStyle.ToolButtonTextUnderIcon)
    
    
    def on_click(self):
        self.signal.emit(True)