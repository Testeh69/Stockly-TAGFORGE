import win32print
from PyQt6.QtWidgets import QPushButton
from PyQt6.QtCore import QSize
from PyQt6.QtGui import QIcon
from ui.elements.styles.style_btn import StyleGenericBtn
from ui.elements.sub_window.menu_print import MenuPrint


class BtnPrint(QPushButton):

    def __init__(self, parent=None, data_to_print:list[dict[str,str]]=None):
        super().__init__( parent)
        self.data_to_print = data_to_print
        self.setIcon(QIcon("assets/print.svg"))  # chemin vers ton icône
        self.setIconSize(QSize(50, 50))
        self.clicked.connect(self.on_click)
        self.data_list = None
        self.setStyleSheet(StyleGenericBtn.apply_style_btn())
        self.display_menu_print = False
        self.menu_print = None if self.display_menu_print == False else MenuPrint()

    def on_click(self):
        result = self.data_to_print()
        if self.display_menu_print == False:
            self.display_menu_print = True
            self.menu_print = MenuPrint(data_to_print=result)
            self.menu_print.show()
        else:
            self.display_menu_print = False
            self.menu_print.close()

