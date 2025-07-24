from PyQt6.QtWidgets import QWidget, QHBoxLayout, QLabel
from PyQt6.QtCore import Qt


class DisplayDataElement(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.label = QLabel("data detected", self)
        self.label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.label.setStyleSheet("color: #bbb;")
        self.layout = QHBoxLayout(self)
        self.layout.setContentsMargins(6, 6, 6, 6)
        self.layout.addWidget(self.label)
        self.setStyleSheet("""
            background-color: rgba(40, 40, 40, 0.6);
            border: 1.5px solid""")
        self.show_data()

    def show_data(self):
        self.label = QLabel("data detected", self)
