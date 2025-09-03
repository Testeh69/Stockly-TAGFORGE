import os 
import pandas as pd

import unicodedata
from PyQt6.QtWidgets import QWidget, QHBoxLayout, QLabel
from PyQt6.QtGui import QFont
from PyQt6.QtCore import Qt, pyqtSignal



class DragDropElement(QWidget):

    signal = pyqtSignal(pd.DataFrame, name = "data")

    def __init__(self, parent=None):
        super().__init__(parent)
       
        self.setAcceptDrops(True)
        self.setFixedSize(200, 200)  

        self.setStyleSheet("""
            background-color: rgba(10, 10, 10, 0.2);
            border: 1.5px dashed #888;
            border-radius: 10px;
            color: #ccc;
        """)


        self.layout = QHBoxLayout(self)
        self.layout.setContentsMargins(6, 6, 6, 6)

        self.label = QLabel("Drag And Drop\nfile", self)
        self.label.setFont(QFont("Segoe UI", 18))
        self.label.setStyleSheet("""color: #bbb;                            """)
        self.label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.layout.addWidget(self.label)

    def dragEnterEvent(self, event):
        if event.mimeData().hasUrls():
            event.accept()
        else:
            event.ignore()

    def dropEvent(self, event):
        urls = event.mimeData().urls()
        print(urls)
        if not urls:
            return 
        path = urls[0].toLocalFile()
        if path.endswith('.xlsx'):
            self.load_excel_file(path)
            print("File loaded successfully:", path)
            self.setVisible(False)
            self.signal.emit(self.data)
       
            

    def normalize_column_name(self,name: str) -> str:
        """Normalise un nom de colonne : minuscules + suppression des accents + suppression des espaces inutiles"""
        name = str(name).strip().lower()
        name = unicodedata.normalize('NFKD', name).encode('ASCII', 'ignore').decode('ASCII')
        return name

    def load_excel_file(self, file_path):
        if not os.path.exists(file_path):
            return None
        try:
            df = pd.read_excel(file_path)

            # Colonnes d'intérêt normalisées
            desired_cols = ["référence", "lot", "designation"]
            desired_cols_norm = [self.normalize_column_name(c) for c in desired_cols]

            # Créer un mapping normalisé -> original
            col_map = {self.normalize_column_name(col): col for col in df.columns}

            # Sélectionner uniquement les colonnes présentes
            selected_cols = [col_map[c] for c in desired_cols_norm if c in col_map]

            self.data = df[selected_cols]

            self.show_data()

        except Exception as e:
            print(f"Error loading Excel file: {e}")
            return None
        

    def show_data(self):
        print(self.data)
        