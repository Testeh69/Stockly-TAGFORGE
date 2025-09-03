from PyQt6.QtWidgets import QPushButton

from PyQt6.QtPrintSupport import QPrinter, QPrintDialog
from PyQt6.QtGui import QTextDocument
from core.qr_system import QRCodeGenerator



class BtnPrint(QPushButton):

    def __init__(self, label: str = "ALL", parent=None, data_to_print=None):
        super().__init__(label, parent)
        self.data_to_print = data_to_print
        self.clicked.connect(self.on_click)
        self.data_list = None
    def on_click(self):
        # Vérifie si data_to_print est callable (une fonction) et l'appelle
        if callable(self.data_to_print):
            self.data_list = self.data_to_print()  # ici on récupère la liste
        else:
            self.data_list = self.data_to_print

        self.print_checked_rows()
  
    
    def print_checked_rows(self):
        if not self.data_list:
            print("⚠ Aucune ligne cochée !")
            return

        all_data = []
        for data in self.data_list:
            data_formatted = f"Lot:{data['lot']}, Designation:{data['designation']}, Reference:{data['reference']}"
            qr_code_path = QRCodeGenerator.generate_qr_code(data_formatted)

            # HTML avec QR + texte
            all_data.append(
                f"<div style='margin-bottom:20px; text-align:center;'>"
                f"<img src='{qr_code_path}' alt='QR Code'><br>"
                f"{data_formatted}</div>"
            )

        # Créer le document HTML
        html_content = "<br>".join(all_data)
        document = QTextDocument()
        document.setHtml(html_content)

        # Boîte de dialogue d’impression
        printer = QPrinter()
        dialog = QPrintDialog(printer, self)
        if dialog.exec():
            document.print(printer)