import pandas as pd
import numpy as np
from PyQt6.QtWidgets import QSizePolicy,QTableWidget,QVBoxLayout, QTableWidgetItem, QWidget, QHBoxLayout
from PyQt6.QtCore import Qt
from ui.elements.btn.btn_check import BtnCheck
from ui.elements.btn.btn_print import BtnPrint
from ui.elements.btn.btn import BtnGen
from ui.elements.search_bar import SearchBarElement
from ui.elements.pop_up_add import PopUpAddItem
from core.utils import normalize_column_name, detect_dark_mode


class DisplayDataElement(QWidget):
    """
    Display and manage a data table with search and action buttons.
    """
    def __init__(self, parent=None):
        """ Initialize the DisplayDataElement."""
        super().__init__(parent)
        print("Initializing DisplayDataElement...")
        is_dark_mode = detect_dark_mode()

        # --- Composants ---
        self.search_bar_element = SearchBarElement()
        self.search_bar_element.search_signal.connect(self.filter_data)
        self.search_bar_element.setFixedHeight(40)

        # --- Boutons ---
        button_config = [
            ("check", BtnCheck, {}, self.on_toggle_all),
            ("print", BtnPrint, {"data_to_print": lambda: self.row_is_checked()}, None),
            ("refresh", BtnGen, {"icon_path": "assets/refresh.svg", "size": 50, "label": "Actualiser"}, self.on_refresh),
            ("add", BtnGen, {"icon_path": "assets/add.svg", "size": 50, "label": "Ajouter"}, self.add_items),
            ("erase", BtnGen, {"icon_path": "assets/bin.svg", "size": 50, "label": "Supprimer"}, self.erase_checked_items),
        ]

        self.buttons = {}

        for btn_config in button_config:
            name, btn = self.create_btn(btn_config)
            self.buttons[name] = btn

        menu = QWidget()
        menu_layout = QVBoxLayout()
        menu_layout.setSpacing(0)
        for btn in self.buttons.values():
            btn.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
            menu_layout.addWidget(btn,1)

        menu.setLayout(menu_layout)

    
        # --- Menu ---
        bg = "#1A1D21" if is_dark_mode else "#0078D7"
        border_color = "#F1F1F1" if is_dark_mode else "#0078D7"
        border_style = "0.5px solid {}".format(border_color)
        border_radius = "8px"
        menu.setObjectName("menu")
        menu.setStyleSheet(f"""
            #menu {{
            border-right: {border_style};
            border-top: {border_style};
            border-bottom:{border_style};
            border-top-right-radius: {border_radius};
            border-bottom-right-radius: {border_radius};
            background-color: {bg};
            }}
        """)
      



        # --- Tableau ---
        self.table = QTableWidget()
        self.table.setMinimumHeight(800)
        self.table.setMinimumWidth(1200)
        self.table.setAlternatingRowColors(True)
        self.table.setShowGrid(True)
        self.table.setEditTriggers(QTableWidget.EditTrigger.DoubleClicked)
        self.table.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        self.table.cellDoubleClicked.connect(self.on_cell_double_clicked)



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


    #--- Création de bouttons:
    def create_btn(self,btn_config):
        name, btn_class, kwargs, callback = btn_config
        btn = btn_class(**kwargs)
        if callback:
            if hasattr(btn, "signal"):
                btn.signal.connect(callback)
            elif hasattr(btn, "toggled_signal"):
                btn.toggled_signal.connect(callback)
        return name, btn

    # --- Gestion édition cellule ---
    def on_cell_double_clicked(self, row, col):
        """Cache temporairement le texte lors de l'édition"""
        item = self.table.item(row, col)
        if item:
            self.previous_value = item.text()
            item.setText("")

    
    def add_items(self):
        """Ajoute une nouvelle ligne via une popup"""
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
                for col, key in enumerate(["reference", "lot","designation"], start=1):
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
        """Affiche les données dans le tableau"""
        if df is None or df.empty:
            self.table.setRowCount(0)
            self.table.setColumnCount(0)
            return

        rows, cols = df.shape
        self.table.setRowCount(rows)
        self.table.setColumnCount(cols + 1)  # +1 pour checkbox

        # Header
        header = ["✔"] + df.columns.astype(str).tolist()
        self.table.setHorizontalHeaderLabels(header)

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
        max_width = 300  # par exemple 300 pixels
        for col in range(self.table.columnCount()):
            if self.table.columnWidth(col) > max_width:
                self.table.setColumnWidth(col, max_width)



    # --- Récupération des lignes cochées ---
    def row_is_checked(self) -> list[dict[str,str]]:
        """Retourne les données des lignes cochées sous forme de liste de dictionnaires"""
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
        """Retourne à la vue principale"""
        parent_window = self.window()
        if hasattr(parent_window, "stackWidget"):
            parent_window.stackWidget.setCurrentIndex(0)