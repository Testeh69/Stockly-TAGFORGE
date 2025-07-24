import os 
import pandas as pd

from PyQt6.QtWidgets import QWidget, QHBoxLayout, QLabel
from PyQt6.QtGui import QFont
from PyQt6.QtCore import Qt, pyqtSignal



class DragDropElement(QWidget):
    data = pyqtSignal(pd.DataFrame)

    def __init__(self, parent=None):
        super().__init__(parent)
       
        self.setAcceptDrops(True)
        self.setFixedSize(200, 200)  

        self.setStyleSheet("""
            background-color: rgba(40, 40, 40, 0.6);
            border: 1.5px dashed #888;
            border-radius: 10px;
            color: #ccc;
        """)

        self.layout = QHBoxLayout(self)
        self.layout.setContentsMargins(6, 6, 6, 6)

        self.label = QLabel("Drag And Drop\nfile", self)
        self.label.setFont(QFont("Segoe UI", 18))
        self.label.setStyleSheet("color: #bbb;")
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
       
            

    def load_excel_file(self, file_path):
        if not os.path.exists(file_path):
            return None
        try:
            df = pd.read_excel(file_path)
            columns = [col for col in df.columns if col in ["Reference", "Lot", "Designation"]]
            self.data = df[columns]
            self.show_data()

        except Exception as e:
            print(f"Error loading Excel file: {e}")
            return None
        

    def show_data(self):
        print(self.data)
        