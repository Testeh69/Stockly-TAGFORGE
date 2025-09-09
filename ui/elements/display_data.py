from PyQt6.QtWidgets import QTableWidget,QVBoxLayout, QTableWidgetItem, QWidget, QHBoxLayout
from PyQt6.QtCore import Qt
import pandas as pd
from ui.elements.btn.btn_check import BtnCheck
from ui.elements.btn.btn_print import BtnPrint
from ui.elements.btn.btn import BtnGen
from ui.elements.search_bar import SearchBarElement
from ui.elements.pop_up_add import PopUpAddItem
from core.utils import normalize_column_name, detect_dark_mode

import numpy as np

class DisplayDataElement(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        is_dark_mode = detect_dark_mode()

        # --- Composants ---
        self.search_bar_element = SearchBarElement()
        self.search_bar_element.search_signal.connect(self.filter_data)
        self.search_bar_element.setFixedHeight(40)

        # --- Boutons ---

        self.btn_check = BtnCheck()
        self.btn_print = BtnPrint(data_to_print=lambda: self.row_is_checked())
        self.btn_refresh = BtnGen(icon_path="assets/refresh.svg", size=50)
        self.btn_add = BtnGen(icon_path="assets/add.svg", size=50)
        self.btn_erase = BtnGen(icon_path="assets/bin.svg", size=50)

        # --- Connexions ---
        self.btn_refresh.signal.connect(self.on_refresh)
        self.btn_check.toggled_signal.connect(self.on_toggle_all)
        self.btn_add.signal.connect(self.add_items)
        self.btn_erase.signal.connect(self.erase_checked_items)

        list_btn = [self.btn_check, self.btn_print, self.btn_refresh, self.btn_add, self.btn_erase]

        for btn in list_btn:
            btn.setFixedSize(60, 60)

        # --- Tableau ---
        self.table = QTableWidget()
        self.table.setMinimumHeight(800)
        self.table.setMinimumWidth(1200)
        self.table.setAlternatingRowColors(True)
        self.table.setShowGrid(True)
        self.table.setEditTriggers(QTableWidget.EditTrigger.DoubleClicked)
        self.table.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        self.table.cellDoubleClicked.connect(self.on_cell_double_clicked)

        # --- Menu ---
        menu = QWidget()
        bg = "#64E9EE" if is_dark_mode else "#0078D7"
        border = "#64E9EE" if is_dark_mode else "#0078D7"
        menu.setStyleSheet(f"""
            border: 1px solid {border};
            border-radius: 8px;
            padding: 8px;
            background-color: {bg};
            transition: background-color 300ms, border-color 300ms;
        """)
        menu_layout = QVBoxLayout()
        menu_layout.setContentsMargins(0, 0, 0, 0)
        menu_layout.setSpacing(0)
        
        menu_layout.addWidget(self.btn_check)
        menu_layout.addWidget(self.btn_print)
        menu_layout.addWidget(self.btn_refresh)
        menu_layout.addWidget(self.btn_add)
        menu_layout.addWidget(self.btn_erase)
        menu.setLayout(menu_layout)

        # --- Layout Secondaire ---
        sub_layout = QHBoxLayout()
        sub_layout.addWidget(menu, alignment=Qt.AlignmentFlag.AlignLeft)
        sub_layout.addWidget(self.table)
        sub_layout.setSpacing(150)
        sub_layout.setContentsMargins(0, 0, 0, 0)
        # --- Layout principal ---
        main_layout = QVBoxLayout(self)
        main_layout.addWidget(self.search_bar_element)
        main_layout.addLayout(sub_layout)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(20)
     

        # --- Données internes ---
        self.data_checked = []
        self.previous_value = None  # Pour restaurer valeur si édition annulée

    # --- Gestion édition cellule ---
    def on_cell_double_clicked(self, row, col):
        """Cache temporairement le texte lors de l'édition"""
        item = self.table.item(row, col)
        if item:
            self.previous_value = item.text()
            item.setText("")

    
    def add_items(self):
        dialog = PopUpAddItem(self)
        if dialog.exec() == PopUpAddItem.DialogCode.Accepted:
            data = dialog.get_data()
            for key in data.keys():
                data[key] = data[key] if data[key].strip() else "N/A"
            if all(data.values()):
                row_position = self.table.rowCount()
                self.table.insertRow(row_position)

                # Checkbox
                checkbox_item = QTableWidgetItem()
                checkbox_item.setFlags(Qt.ItemFlag.ItemIsUserCheckable | Qt.ItemFlag.ItemIsEnabled)
                checkbox_item.setCheckState(Qt.CheckState.Checked if self.btn_check.isChecked() else Qt.CheckState.Unchecked)
                self.table.setItem(row_position, 0, checkbox_item)

                # Données
                for col, key in enumerate(["reference", "designation", "lot"], start=1):
                    item = QTableWidgetItem(data[key]) if data[key] else QTableWidgetItem("N/A")
                    item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
                    self.table.setItem(row_position, col, item)
                self.table.resizeColumnsToContents()
            else:
                print("⚠ Tous les champs doivent être remplis !")

    def erase_checked_items(self):
        """Supprime les lignes cochées"""
        rows_to_erase = []
        for row in range(self.table.rowCount()):
            checkbox_item = self.table.item(row, 0)
            if checkbox_item and checkbox_item.checkState() == Qt.CheckState.Checked:
                rows_to_erase.append(row)

        for row in reversed(rows_to_erase):
            self.table.removeRow(row)


    # --- Affichage des données ---
    def show_data(self, df: pd.DataFrame):
        if df is None or df.empty:
            self.table.setRowCount(0)
            self.table.setColumnCount(0)
            return

        rows, cols = df.shape
        self.table.setRowCount(rows)
        self.table.setColumnCount(cols + 1)  # +1 pour checkbox

        # Header
        self.table.setHorizontalHeaderLabels(["✔"] + df.columns.astype(str).tolist())

        for row in range(rows):
            # Checkbox
            checkbox_item = QTableWidgetItem()
            checkbox_item.setFlags(Qt.ItemFlag.ItemIsUserCheckable | Qt.ItemFlag.ItemIsEnabled)
            checkbox_item.setCheckState(Qt.CheckState.Checked if self.btn_check.isChecked() else Qt.CheckState.Unchecked)
            self.table.setItem(row, 0, checkbox_item)

            # Données
            for col in range(cols):
                val = str(df.iat[row, col])
                item = QTableWidgetItem(val)
                item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
                self.table.setItem(row, col + 1, item)

        self.table.resizeColumnsToContents()



    # --- Récupération des lignes cochées ---
    def row_is_checked(self):
        self.data_checked = []

        headers = {normalize_column_name(self.table.horizontalHeaderItem(col).text()): col
                   for col in range(self.table.columnCount())
                   if self.table.horizontalHeaderItem(col)}

        required_cols = ["lot", "designation", "reference"]
        if not all(col in headers for col in required_cols):
            print("⚠ Colonnes manquantes dans le tableau !")
            return []

        for row in range(self.table.rowCount()):
            checkbox_item = self.table.item(row, 0)
            if checkbox_item and checkbox_item.checkState() == Qt.CheckState.Checked:
                data = {col: self.table.item(row, headers[col]).text() for col in required_cols}
                self.data_checked.append(data)
        return self.data_checked

    # --- Toggle toutes les cases ---
    def on_toggle_all(self, checked: bool):
        for row in range(self.table.rowCount()):
            item = self.table.item(row, 0)
            if item:
                item.setCheckState(Qt.CheckState.Checked if checked else Qt.CheckState.Unchecked)


    # --- Filtrage par recherche ---
    def filter_data(self, text: str):
        """Filtre les lignes en fonction du texte de recherche"""
        text = text.lower()
        for row in range(self.table.rowCount()):
            match = any(text in self.table.item(row, col).text().lower()
                        for col in range(1, self.table.columnCount()))
            self.table.setRowHidden(row, not match)

    # --- Rafraîchissement ---
    def on_refresh(self):
        parent_window = self.window()
        if hasattr(parent_window, "stackWidget"):
            parent_window.stackWidget.setCurrentIndex(0)