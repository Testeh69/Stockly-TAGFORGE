from PyQt6.QtWidgets import QMainWindow, QWidget, QVBoxLayout, QLabel, QSplitter
from PyQt6.QtGui import QIcon, QPixmap
from PyQt6.QtCore import Qt
from ui.subQrWindow import QrCodeWindowLeft as QrCodeWindow
from controllers.qr_system import QRCodeGenerator

class StockTagForgeMainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("STOCKLY TAGFORGE")
        self.setGeometry(100, 100, 500, 200)
        self.setWindowIcon(QIcon("assets/logo.png"))

        self.qr_generator = QRCodeGenerator()
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        self.main_layout = QVBoxLayout(self.central_widget)
        self.splitter = QSplitter(Qt.Orientation.Horizontal)

        self._setup_main_ui()

    def keyPressEvent(self, event):
        if event.key() == Qt.Key.Key_Escape:
            self.showNormal()
        elif event.key() == Qt.Key.Key_F11:
            self.showFullScreen()

    def _setup_main_ui(self):
        # Panneau gauche : formulaire
        self.qr_code_panel = QrCodeWindow()
        self.splitter.addWidget(self.qr_code_panel)

        # Panneau droit : affichage QR code
        self.qr_preview = QLabel("QR Code Preview")
        self.qr_preview.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.qr_preview.setStyleSheet("background-color: #f0f0f0; border: 1px solid #ccc;")
        self.splitter.addWidget(self.qr_preview)

        # Ajout du splitter au layout principal
        self.main_layout.addWidget(self.splitter)

        # Pied de page
        footer_label = QLabel("© 2024 STOCKLY TAGFORGE. Tous droits réservés.")
        footer_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.main_layout.addWidget(footer_label)

    def update_qr_preview(self, image_path: str):
        pixmap = QPixmap(image_path)
        self.qr_preview.setPixmap(pixmap.scaled(300, 300, Qt.AspectRatioMode.KeepAspectRatio))
