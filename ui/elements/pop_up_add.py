from PyQt6.QtWidgets import (
   QVBoxLayout, QHBoxLayout, QDialog, QLabel, QLineEdit, QDialogButtonBox
)

class PopUpAddItem(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Ajouter un élément")
        self.setModal(True)

        # Création des champs
        self.reference_input = QLineEdit()
        self.designation_input = QLineEdit()
        self.lot_input = QLineEdit()

        # Layout des labels et champs
        layout = QVBoxLayout()
        for label_text, widget in [("Référence", self.reference_input),
                                   ("Désignation", self.designation_input),
                                   ("Lot", self.lot_input)]:
            hlayout = QHBoxLayout()
            hlayout.addWidget(QLabel(label_text))
            hlayout.addWidget(widget)
            layout.addLayout(hlayout)

        # Boutons OK / Annuler
        buttons = QDialogButtonBox(QDialogButtonBox.StandardButton.Ok | 
                                   QDialogButtonBox.StandardButton.Cancel)
        buttons.accepted.connect(self.accept)
        buttons.rejected.connect(self.reject)
        layout.addWidget(buttons)

        self.setLayout(layout)

    def get_data(self):
        """Retourne un dictionnaire des valeurs saisies"""
        return {
            "reference": self.reference_input.text(),
            "designation": self.designation_input.text(),
            "lot": self.lot_input.text()
        }