from PyQt6.QtWidgets import QPushButton
from PyQt6.QtGui import QIcon

class Button(QPushButton):
    def __init__(self, text: str, icon_path: str = None, dimensions: tuple[int, int] = (100, 50), style: str = None, function = None):
        super().__init__(text)
        self.setMinimumSize(dimensions[0], dimensions[1])

        if icon_path:
            self.setIcon(QIcon(icon_path))

        if style:
            self.setStyleSheet(style)

        if function:
            self.clicked.connect(function)