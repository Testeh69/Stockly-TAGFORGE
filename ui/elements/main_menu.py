
from PyQt6.QtWidgets import QWidget, QVBoxLayout
from PyQt6.QtCore import Qt

from ui.elements.btn.btn_check import BtnCheck
from ui.elements.btn.btn_print import BtnPrint
from ui.elements.btn.btn import BtnGen
from core.utils import detect_dark_mode


class SideMenuElement(QWidget):

    def __init__(self, parent=None, print_callback=None, on_data_ready=None):
        super().__init__(parent)

        is_dark_mode = detect_dark_mode()

        # --- Création des boutons ---
        self.btn_check = BtnCheck()
        self.btn_print = BtnPrint(data_to_print=print_callback)

        self.btn_refresh = BtnGen(
            icon_path="assets/refresh.svg",
            text="ACTUALISER",
            size=50
        )

        self.btn_add = BtnGen(
            icon_path="assets/add.svg",
            text="AJOUTER",
            size=50
        )

        self.btn_erase = BtnGen(
            icon_path="assets/bin.svg",
            text="SUPPRIMER",
            size=50
        )

        self.btn_save = BtnGen(
            icon_path="assets/save.svg",
            text="SAUVEGARDER",
            size=50
        )

        self.list_btn = [
            self.btn_check,
            self.btn_print,
            self.btn_refresh,
            self.btn_add,
            self.btn_erase,
            self.btn_save
        ]

        # --- Dimensions ---
        self.setFixedWidth(190)

        # --- Layout ---
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        for index, btn in enumerate(self.list_btn):

            # Même largeur pour tous les boutons
            btn.setFixedWidth(190)
            btn.setMinimumHeight(48)

            layout.addWidget(btn)

        # --- Palette ---
        if is_dark_mode:
            background = "#172033"
            border = "#293750"
            button_bg = "#172033"
            hover = "#24344D"
            accent = "#64E9EE"
            text = "#EAF2FA"
            separator = "#293750"
        else:
            background = "#F4F7FC"
            border = "#DCE4EF"
            button_bg = "#F4F7FC"
            hover = "#E5F0FC"
            accent = "#0078D7"
            text = "#243247"
            separator = "#DCE4EF"

        # --- Style global ---
        self.setObjectName("sideMenu")

        self.setStyleSheet(f"""
            QWidget#sideMenu {{
                background-color: {background};
                border: 1px solid {border};
                border-radius: 10px;
            }}

            QWidget#sideMenu QToolButton,
            QWidget#sideMenu QPushButton {{
                background-color: {button_bg};
                color: {text};
                border: none;
                border-bottom: 1px solid {separator};
                border-radius: 0px;
                padding: 10px 14px;
                font-family: "Segoe UI";
                font-size: 10px;
                font-weight: 600;
                text-align: left;
            }}

            QWidget#sideMenu QToolButton:hover,
            QWidget#sideMenu QPushButton:hover {{
                background-color: {hover};
                color: {accent};
                border-left: 3px solid {accent};
            }}

            QWidget#sideMenu QToolButton:pressed,
            QWidget#sideMenu QPushButton:pressed {{
                background-color: {background};
                color: {accent};
            }}

            QWidget#sideMenu QToolButton:last-child,
            QWidget#sideMenu QPushButton:last-child {{
                border-bottom: none;
            }}
        """)
