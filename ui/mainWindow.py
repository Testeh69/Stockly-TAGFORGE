from PyQt6.QtWidgets import QMainWindow, QWidget, QVBoxLayout, QLabel
from PyQt6.QtGui import QIcon
from PyQt6.QtCore import Qt
from ui.subQrWindow import QrCodeWindow
from controllers.qr_system import QRCodeGenerator

class StockTagForgeMainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("STOCKLY TAGFORGE - Application Principale")
        self.setGeometry(100, 100, 800, 600)
        self.setWindowIcon(QIcon("assets/icon.png")) # Chemin vers votre icône

        self.qr_generator = QRCodeGenerator() # Instanciation du Modèle

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.main_layout = QVBoxLayout(self.central_widget)

        self._setup_main_ui()

    def _setup_main_ui(self):
        # Exemple: Un titre ou une barre d'en-tête pour la fenêtre principale
        title_label = QLabel("Bienvenue sur STOCKLY TAGFORGE !")
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title_label.setStyleSheet("font-size: 24px; font-weight: bold; margin-bottom: 20px;")
        self.main_layout.addWidget(title_label)
        
        # Instancier et ajouter le QrCodeWindow à la disposition principale
        self.qr_code_panel = QrCodeWindow()
        self.main_layout.addWidget(self.qr_code_panel)

        # Facultatif: Ajouter un pied de page ou d'autres éléments à la fenêtre principale
        footer_label = QLabel("© 2024 STOCKLY TAGFORGE. Tous droits réservés.")
        footer_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.main_layout.addWidget(footer_label)