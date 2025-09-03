from PyQt6.QtWidgets import QTableWidget,QVBoxLayout, QTableWidgetItem, QWidget, QHBoxLayout, QLabel
from PyQt6.QtCore import Qt
import pandas as pd
from ui.elements.btn_check import BtnCheck
from ui.elements.btn_print import BtnPrint
from core.utils import normalize_column_name

class DisplayDataElement(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.qr_code_data = []
        self.btn_check = BtnCheck("Select All")
        self.btn_print = BtnPrint("Print Selected", data_to_print=lambda: self.row_is_checked())
        self.table = QTableWidget()

        # Connecter le bouton au slot
        self.btn_check.toggled_signal.connect(self.on_toggle_all)

        layout = QVBoxLayout(self)
        layout.addWidget(self.table)
        layout.addWidget(self.btn_check)
        layout.addWidget(self.btn_print)
        
        self.table.setAlternatingRowColors(True)
        self.table.setShowGrid(True)
        self.table.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
        self.table.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)

    def show_data(self, df: pd.DataFrame):
        if df is None or df.empty:
            self.table.setRowCount(0)
            self.table.setColumnCount(0)
            return

        rows = len(df)
        cols = len(df.columns)

        self.table.setRowCount(rows)
        self.table.setColumnCount(cols + 1)  # +1 pour les cases à cocher

        self.table.setHorizontalHeaderLabels(["✔"] + df.columns.astype(str).tolist())

        for row in range(rows):
            checkbox_item = QTableWidgetItem()
            checkbox_item.setFlags(Qt.ItemFlag.ItemIsUserCheckable | Qt.ItemFlag.ItemIsEnabled)
            checkbox_item.setCheckState(Qt.CheckState.Unchecked)
            self.table.setItem(row, 0, checkbox_item)
            if self.on_toggle_all:
                checkbox_item.setCheckState(Qt.CheckState.Checked)
            for col in range(cols):
                val = str(df.iat[row, col])
                item = QTableWidgetItem(val)
                item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
                self.table.setItem(row, col + 1, item)

        self.table.resizeColumnsToContents()
    

    def row_is_checked(self):
       

        self.qr_code_data = []  # reset à chaque appel

        # Dictionnaire normalisé : nom colonne -> index
        headers = {}
        for col in range(self.table.columnCount()):
            header_item = self.table.horizontalHeaderItem(col)
            if header_item is not None:
                normalized = normalize_column_name(header_item.text())
                headers[normalized] = col

        # Colonnes nécessaires normalisées
        required_cols = ["lot", "designation", "reference"]
        if not all(col in headers for col in required_cols):
            print("⚠ Colonnes manquantes dans le tableau !")
            return []

        for row in range(self.table.rowCount()):
            checkbox_item = self.table.item(row, 0)  # première colonne = checkbox
            if checkbox_item is not None and checkbox_item.checkState() == Qt.CheckState.Checked:
                lot = self.table.item(row, headers["lot"]).text()
                designation = self.table.item(row, headers["designation"]).text()
                reference = self.table.item(row, headers["reference"]).text()

                data = {"lot": lot, "designation": designation, "reference": reference}
                self.qr_code_data.append(data)
        return self.qr_code_data

    def on_toggle_all(self, checked: bool):
        """Coche/décoche toutes les cases"""
        for row in range(self.table.rowCount()):
            item = self.table.item(row, 0)
            if item is not None:
                item.setCheckState(Qt.CheckState.Checked if checked else Qt.CheckState.Unchecked)