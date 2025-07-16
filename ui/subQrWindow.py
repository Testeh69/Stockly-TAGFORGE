from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout,
    QLineEdit, QPushButton, QLabel, QMessageBox,
    QFormLayout 
)
from PyQt6.QtGui import QPixmap, QPainter
from PyQt6.QtCore import Qt
from PyQt6.QtPrintSupport import QPrinter, QPrintDialog
from controllers.qr_system import QRCodeGenerator

class QrCodeWindowLeft(QWidget):

    def __init__(self, func = QRCodeGenerator):
        super().__init__(parent=None)
        self.qr_generator = func
        self.current_qrcode_pixmap = None 
        self.data_parts = []
        self.path = None  
        self._setup_ui()

    
    def _setup_ui(self):
        main_layout = QHBoxLayout(self) # 

        input_controls_layout = QVBoxLayout()
        main_layout.addLayout(input_controls_layout)

        form_layout = QFormLayout()
        
        self.field_nom_produit = QLineEdit()
        self.field_nom_produit.setPlaceholderText("Nom du produit")
        form_layout.addRow("Nom du produit:", self.field_nom_produit)
        self.field_reference = QLineEdit()
        self.field_reference.setPlaceholderText("Référence produit")
        form_layout.addRow("Référence:", self.field_reference)

        self.field_designation = QLineEdit()
        self.field_designation.setPlaceholderText("Désignation")
        form_layout.addRow("Désignation:", self.field_designation)
        

        input_controls_layout.addLayout(form_layout)

  
        self.generate_button = QPushButton("Générer QR Code")
        self.generate_button.clicked.connect(self._on_generate_qr_code_clicked)
        input_controls_layout.addWidget(self.generate_button)

        self.print_button = QPushButton("Imprimer le QR Code")
        self.print_button.clicked.connect(self._on_generate_qr_code_clicked)
        self.print_button.setEnabled(False) # Désactivé par défaut
        input_controls_layout.addWidget(self.print_button)


    def _on_generate_qr_code_clicked(self):
        self.data_parts = []
        self.data_parts.append(f"Lot:{self.field_nom_produit.text()}")
        self.data_parts.append(f"Designation:{self.field_reference.text()}")
        self.data_parts.append(f"Reference: {self.field_designation.text()}")
   
        data_to_encode = " ,".join(self.data_parts)
        self.path = "qr_code.png" 
        response = self.qr_generator.generate_qr_code(data_to_encode, self.path)
