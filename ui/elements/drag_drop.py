from PyQt6.QtWidgets import QWidget, QHBoxLayout, QLabel
from PyQt6.QtGui import QFont
from PyQt6.QtCore import Qt


class DragDropElement(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setAcceptDrops(True)
        self.setFixedSize(200, 200)  # Taille réduite

        # Style moderne : fond gris foncé translucide + bordure fine + arrondie
        self.setStyleSheet("""
            background-color: rgba(40, 40, 40, 0.6);
            border: 1.5px dashed #888;
            border-radius: 10px;
            color: #ccc;
        """)

        self.layout = QHBoxLayout(self)
        self.layout.setContentsMargins(6, 6, 6, 6)

        self.label = QLabel("Drag And Drop\nfile", self)
        self.label.setFont(QFont("Segoe UI", 18))
        self.label.setStyleSheet("color: #bbb;")
        self.label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.layout.addWidget(self.label)

    def dragEnterEvent(self, event):
        if event.mimeData().hasUrls():
            event.accept()
        else:
            event.ignore()

    def dropEvent(self, event):
        if event.mimeData().hasUrls():
            urls = event.mimeData().urls()
            for url in urls:
                print(f"Dropped file: {url.toLocalFile()}")
            event.accept()
        else:
            event.ignore()