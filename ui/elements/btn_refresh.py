


from PyQt6.QtWidgets import QPushButton
from PyQt6.QtCore import pyqtSignal, Qt



class BtnRefresh(QPushButton):

    refresh_signal = pyqtSignal(bool)

    def __init__(self, label: str = "ALL", parent=None):
        super().__init__(label, parent)
        self.clicked.connect(self.on_click)
      
    
    
    def on_click(self):
        self.refresh_signal.emit(True)

       
  
    
    