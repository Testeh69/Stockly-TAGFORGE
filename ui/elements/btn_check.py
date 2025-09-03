from PyQt6.QtWidgets import QPushButton
from PyQt6.QtCore import pyqtSignal, Qt





class BtnCheck(QPushButton):
    toggled_signal = pyqtSignal(bool)

    def __init__(self, label: str = "ALL", parent=None):
        super().__init__(label, parent)
        self.setCheckable(True)
        self.setChecked(False)
        self.clicked.connect(self.on_click)

    def on_click(self):
        checked = self.isChecked()
        self.toggled_signal.emit(checked)
        self.update_style()

    def update_style(self):
        if self.isChecked():
            self.setStyleSheet("background-color: green; color: white;")
        else:
            self.setStyleSheet("background-color: none; color: black;")