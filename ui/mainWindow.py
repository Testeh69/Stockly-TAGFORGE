from PyQt6.QtWidgets import QMainWindow, QWidget, QVBoxLayout
from PyQt6.QtGui import QIcon
from PyQt6.QtCore import Qt


from ui.elements.drag_drop import DragDropElement


class StockTagForgeMainWindow(QMainWindow):
    def __init__(self, title:str = "STOCKLY TAGFORGE", icon_path:str = "assets/logo.png", dimensions:list[int] = (1000, 800)):
        super().__init__()
        self.file = None
        self.setWindowTitle(title)
        self.setGeometry(100, 100, dimensions[0], dimensions[1])
        self.setMinimumSize(500, 200)   
        self.setWindowIcon(QIcon(icon_path))
        self._setup_main_ui()



    def _setup_main_ui(self):
        central_widget = QWidget(self)
        layout = QVBoxLayout()
        self.drag_drop_element = DragDropElement(self)
        layout.addWidget(self.drag_drop_element, alignment=Qt.AlignmentFlag.AlignCenter)
        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)
        