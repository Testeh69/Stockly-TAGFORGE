from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout,
    QLineEdit, QPushButton, QLabel, QMessageBox,
    QFormLayout # Ajout pour un questionnaire simple
)
from PyQt6.QtGui import QPixmap, QPainter
from PyQt6.QtCore import Qt
from PyQt6.QtPrintSupport import QPrinter, QPrintDialog
from controllers.qr_system import QRCodeGenerator


class QrCodeWindow(QWidget):

    def __init__(self, func = QRCodeGenerator):
        super().__init__(parent=None)
        self.qr_generator = func
        self.current_qrcode_pixmap = None 
        self.data_parts = []  # Pour stocker les données du questionnaire
        self._setup_ui()

    
    def _setup_ui(self):
        main_layout = QHBoxLayout(self) # Layout principal pour cette sous-fenêtre

        # --- Partie Gauche : Questionnaire et Contrôles ---
        input_controls_layout = QVBoxLayout()
        main_layout.addLayout(input_controls_layout)

        # Formulaire du questionnaire
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

        # Boutons d'action
        self.generate_button = QPushButton("Générer QR Code")
        self.generate_button.clicked.connect(self._on_generate_qr_code_clicked)
        input_controls_layout.addWidget(self.generate_button)

        self.print_button = QPushButton("Imprimer le QR Code")
        self.print_button.clicked.connect(self._on_print_qr_code_clicked)
        self.print_button.setEnabled(False) # Désactivé par défaut
        input_controls_layout.addWidget(self.print_button)

        self.status_label = QLabel("Prêt à générer.")
        input_controls_layout.addWidget(self.status_label)


        qr_display_layout = QVBoxLayout()
        main_layout.addLayout(qr_display_layout)

        self.qr_code_display = QLabel("Le QR Code apparaîtra ici")
        self.qr_code_display.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.qr_code_display.setMinimumSize(250, 250)
        self.qr_code_display.setMaximumSize(300, 300)
        qr_display_layout.addWidget(self.qr_code_display)
        
        qr_display_layout.addStretch() 


    def _on_generate_qr_code_clicked(self):
        self.data_parts = []
        self.data_parts.append(f"Lot:{self.field_nom_produit.text()}")
        self.data_parts.append(f"Designation:{self.field_reference.text()}")
        self.data_parts.append(f"Reference: {self.field_designation.text()}")
   
        data_to_encode = " ,".join(self.data_parts) 
        
        if not data_to_encode.strip(): 
            QMessageBox.warning(self, "Erreur de saisie", "Veuillez remplir au moins un champ pour générer le QR Code.")
            self.status_label.setText("Veuillez entrer des données.")
            return

        try:
            pixmap = self.qr_generator.generate_qrcode_image(data_to_encode)
            
       
            scaled_pixmap = pixmap.scaled(
                self.qr_code_display.width(), self.qr_code_display.height(),
                Qt.AspectRatioMode.KeepAspectRatio,
                Qt.TransformationMode.SmoothTransformation
            )
            self.qr_code_display.setPixmap(scaled_pixmap)
            self.current_qrcode_pixmap = pixmap 

            self.print_button.setEnabled(True)
            self.status_label.setText("QR Code généré avec succès !")

        except ValueError as e:
            QMessageBox.warning(self, "Erreur de génération", str(e))
            self.qr_code_display.setText("Erreur lors de la génération.")
            self.print_button.setEnabled(False)
            self.status_label.setText("Erreur de génération.")
        except Exception as e:
            QMessageBox.critical(self, "Erreur inattendue", f"Une erreur inattendue est survenue : {e}")
            self.qr_code_display.setText("Erreur inattendue.")
            self.print_button.setEnabled(False)
            self.status_label.setText("Erreur inattendue.")

    def _on_print_qr_code_clicked(self):
        if not self.current_qrcode_pixmap:
            QMessageBox.warning(self, "Erreur d'impression", "Aucun QR Code à imprimer. Veuillez en générer un d'abord.")
            return

        printer = QPrinter(QPrinter.PrinterMode.HighResolution)
        print_dialog = QPrintDialog(printer, self)

        if print_dialog.exec() == QPrintDialog.DialogCode.Accepted:
            painter = QPainter()
            painter.begin(printer)
            
            # Ajustement de la taille et positionnement du QR code sur la page
            qr_size = self.current_qrcode_pixmap.size()
            page_rect = painter.viewport() # Zone imprimable

            scale_factor = (page_rect.width() * 0.4) / qr_size.width()
            target_width = int(qr_size.width() * scale_factor)
            target_height = int(qr_size.height() * scale_factor)

            # Centrer le QR code sur la page
            x = page_rect.center().x() - target_width // 2
            y = page_rect.center().y() - target_height // 2
            
            painter.drawPixmap(x, y, target_width, target_height, self.current_qrcode_pixmap)
            
            # Facultatif: Ajouter le texte encodé sous le QR code
            painter.setFont(self.font()) # Utilise la police par défaut de la fenêtre
            painter.drawText(x, y + target_height + 20, "Données: " + "\n".join(self.data_parts)) # Position juste en dessous

            painter.end()
            QMessageBox.information(self, "Impression", "Le QR Code a été envoyé à l'imprimante.")
            self.status_label.setText("QR Code imprimé !")
        else:
            QMessageBox.information(self, "Impression", "Impression annulée.")
            self.status_label.setText("Impression annulée.")


        