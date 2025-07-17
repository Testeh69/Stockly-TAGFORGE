from PyQt6.QtWidgets import QWidget, QFormLayout, QLineEdit
from ui.elements.btn import Button
from core.qr_system import QRCodeGenerator


class Forms(QWidget):
    def __init__(self, list_forms: list[str] = None):
        super().__init__()

        self.list_forms = list_forms or ["Nom", "Référence", "Désignation"]
        self.layout = QFormLayout()
        self.setStyleSheet("""
            margin : 20 px;
            font-size: 20px;
        """)

        self.setLayout(self.layout)
        self.fields = {}
        self._setup_ui()

    def _setup_ui(self, path:str = "generic_qr_code.png"):
        for form in self.list_forms:
            self.fields[form] = QLineEdit()
            self.fields[form].setPlaceholderText(f"{form} du produit")
            self.layout.addRow(f"{form} :", self.fields[form])
        btn = Button("Générer le QR Code", icon_path="assets/icons/qr_code.png", dimensions=(200, 30))
        btn.setStyleSheet("""
                QPushButton {
                    background-color: #f0f0f0;
                    color: black;
                    border: none;
                
                    padding: 10px 20px;
                    border-radius: 8px;
                }
                QPushButton:hover {
                    background-color: #0f0f0f;
                    color: white;
                }
                QPushButton:pressed {
                    background-color: #004080;
                }
            """)
        
        btn.clicked.connect(self.get_text_to_qr)

        self.layout.addRow("", btn)
    

    def get_text_to_qr(self):
        data = []
        for form_name, value in self.fields.items():
            value = value.text().strip()
            if value:
                data.append(value)
        data_to_encode = " ,".join(data)
        answer = QRCodeGenerator.generate_qr_code(data_to_encode)
        return answer


