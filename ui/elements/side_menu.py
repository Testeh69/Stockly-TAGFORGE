from PyQt6.QtWidgets import QWidget, QVBoxLayout,QLabel
from PyQt6.QtGui import QPixmap, QIcon
from PyQt6.QtCore import Qt



title_menu = {
    "Stockly TagForge": "assets/logo.png"
}

elements = {
    "Qr Code":"assets/qr_code.svg",
    "Archive": "assets/archive.svg",
    "Settings": "assets/settings.svg",
}



class SideMenu(QWidget):
    def __init__(self, dimensions: tuple[int] = (200, 800),state:bool = True, 
                 title_menu: dict[str,str] = title_menu,  
                 menu_elements: dict[str,str]= elements):
        
        
        super().__init__()
        self.setStyleSheet("""
            background-color: #f0f0f0;
            border: 1px solid #ddd;
            border-radius: 10px;
        """)        
        self.setMinimumSize(dimensions[0], dimensions[1])
        self.state = state
        self.title_menu = title_menu
        self.menu_elements = menu_elements
        self.layouts = QVBoxLayout()
        self._setup_ui()
    

    def _setup_ui(self):
        self.add_title()
    

    def add_title(self):
        for title, icon_path in self.title_menu.items():
            title_label = QLabel(title)
            title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
            title_label.setStyleSheet("font-size: 20px; font-weight: bold; padding: 10px;")
            if icon_path:
                icon = QPixmap(icon_path)
                title_label.setPixmap(icon.scaled(50, 50, Qt.AspectRatioMode.KeepAspectRatio))
            self.layouts.addWidget(title_label)
        
        self.setLayout(self.layouts)





