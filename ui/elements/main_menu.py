from PyQt6.QtWidgets import QWidget, QVBoxLayout
from PyQt6.QtCore import Qt
from ui.elements.btn.btn_check import BtnCheck
from ui.elements.btn.btn_print import BtnPrint
from ui.elements.btn.btn import BtnGen
from core.utils import detect_dark_mode

class SideMenuElement(QWidget):
    def __init__(self, parent=None, print_callback=None):
        super().__init__(parent)
        
        is_dark_mode = detect_dark_mode()
        
        # --- Création des boutons ---
        self.btn_check = BtnCheck()
        # On passe la fonction de callback pour le bouton print
        self.btn_print = BtnPrint(data_to_print=print_callback)
        self.btn_refresh = BtnGen(icon_path="assets/refresh.svg", text = "ACTUALISER", size=50)
        self.btn_add = BtnGen(icon_path="assets/add.svg", text="AJOUTER", size=50)
        self.btn_erase = BtnGen(icon_path="assets/bin.svg", text="SUPPRIMER", size=50, style = f"border-bottom-right-radius:5px;")

        self.list_btn = [self.btn_check, self.btn_print, self.btn_refresh, self.btn_add, self.btn_erase]
        
       

        # --- Layout & Style ---
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        layout.addStretch()  # Pour pousser les boutons vers le haut
        
        for btn in self.list_btn:
            layout.addWidget(btn)
            
        # --- Style ---
        bg = "#64E9EE" if is_dark_mode else "#0078D7"
        self.setStyleSheet(f"""
            SideMenuElement {{
                background-color: {bg};
                border-radius: 8px;
            }}
            /* Style pour que les boutons soient plus beaux quand ils sont larges */
            QToolButton, QPushButton {{
                background-color: rgba(255, 255, 255, 0.2);
                border:None;
                color: white;
                font-weight: bold;
                width: 100%; /* Force visuelle */
            }}
        """)