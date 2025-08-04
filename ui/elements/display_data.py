from PyQt6.QtWidgets import QTableWidget,QVBoxLayout, QTableWidgetItem, QWidget, QHBoxLayout, QLabel
from PyQt6.QtCore import Qt
import pandas as pd

class DisplayDataElement(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.table = QTableWidget()
        layout = QVBoxLayout(self)
        layout.addWidget(self.table)

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

        # Nom des colonnes : on ajoute "✔" ou "Sélection"
        self.table.setHorizontalHeaderLabels(["✔"] + df.columns.astype(str).tolist())

        for row in range(rows):
            # ➤ Case à cocher (colonne 0)
            checkbox_item = QTableWidgetItem()
            checkbox_item.setFlags(Qt.ItemFlag.ItemIsUserCheckable | Qt.ItemFlag.ItemIsEnabled)
            checkbox_item.setCheckState(Qt.CheckState.Unchecked)
            self.table.setItem(row, 0, checkbox_item)

            # ➤ Les données
            for col in range(cols):
                val = str(df.iat[row, col])
                item = QTableWidgetItem(val)
                item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
                self.table.setItem(row, col + 1, item)

        self.table.resizeColumnsToContents()