from PyQt6.QtWidgets import QLineEdit
from PyQt6.QtCore import pyqtSignal
from PyQt6.QtGui import QIcon, QAction
from core.utils import detect_dark_mode



class SearchBarElement(QLineEdit):


    search_signal = pyqtSignal(str, name="search")

    def __init__(self, parent=None):
        super().__init__(parent)
        self.background_color = "rgba(10, 10, 10, 0.2)" if detect_dark_mode() else "rgba(240, 240, 240, 0.8)"
        self.border_color = "#64E9EE" if detect_dark_mode() else "#0078D7"
        self.setStyleSheet(f"""
            QLineEdit {{
                height: 30px;
                font-size: 14px;
                width:100%;
                background-color: {self.background_color};
                border: 1.5px solid {self.border_color};
                border-radius: 5px;
                padding: 5px 10px;
            }}
            QLineEdit:focus {{
                border: 2px solid {self.border_color};
            }}
        """)
        search_action = QAction(QIcon("assets/search.svg"), "", self)
        self.addAction(search_action, QLineEdit.ActionPosition.LeadingPosition)        
        self.setPlaceholderText("Rechercher...")
        self.setClearButtonEnabled(True)
        self.textChanged.connect(self.on_text_changed)

    def on_text_changed(self, text):
        self.search_signal.emit(text)
