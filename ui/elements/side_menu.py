from PyQt6.QtWidgets import QWidget, QVBoxLayout,QLabel


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
        self.setMinimumSize(dimensions[0], dimensions[1])
        self.state = state
        self.title_menu = title_menu
        self.menu_elements = menu_elements
        self._setup_ui()

    def _setup_ui(self):
        pass




