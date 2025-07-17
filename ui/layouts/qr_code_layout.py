from PyQt6.QtWidgets import QWidget, QHBoxLayout
from PyQt6.QtCore import Qt
from ui.elements.forms import Forms

class QRCodeLayout(QWidget):

    def __init__(self, dimensions: tuple[int] = (400, 400)):
        super().__init__()
        self.setMinimumSize(dimensions[0], dimensions[1])
        
        self._setup_ui()

    def _setup_ui(self):
        layout = QHBoxLayout(self)
        self.forms = Forms()
        layout.addWidget(self.forms, alignment=Qt.AlignmentFlag.AlignCenter)
        self.setLayout(layout)
