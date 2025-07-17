from PyQt6.QtWidgets import QMainWindow, QWidget, QHBoxLayout, QLabel
from PyQt6.QtGui import QIcon
from PyQt6.QtCore import Qt
from ui.elements.side_menu import SideMenu
from ui.layouts.qr_code_layout import QRCodeLayout

class StockTagForgeMainWindow(QMainWindow):
    def __init__(self, title:str = "STOCKLY TAGFORGE", icon_path:str = "assets/logo.png", dimensions:list[int] = (1000, 800)):
        super().__init__()
        self.setWindowTitle(title)
        self.setGeometry(100, 100, dimensions[0], dimensions[1])
        self.setMinimumSize(500, 200)   
        self.setWindowIcon(QIcon(icon_path))
        self._setup_main_ui()



    def _setup_main_ui(self):
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QHBoxLayout(central_widget)
        side_menu = SideMenu(dimensions=(200, 200))
        layout.addWidget(side_menu, alignment=Qt.AlignmentFlag.AlignLeft)
        qr_code_layout = QRCodeLayout(dimensions=(800, 600))
        layout.addWidget(qr_code_layout, alignment=Qt.AlignmentFlag.AlignCenter)

       