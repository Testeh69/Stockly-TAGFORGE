from PyQt6.QtWidgets import QStackedWidget,QMainWindow, QVBoxLayout,QWidget,QHBoxLayout , QStackedWidget
from PyQt6.QtGui import QIcon
from PyQt6.QtCore import Qt

from ui.elements.drag_drop import DragDropElement
from ui.elements.display_data import DisplayDataElement

class StockTagForgeMainWindow(QMainWindow):
    def __init__(self, title:str = "STOCKLY TAGFORGE", icon_path:str = "assets/logo.png", dimensions:list[int] = (1000, 800)):
        """
        Initialize the main window with a title, icon, and dimensions.
        """
        super().__init__()
        self.setWindowTitle(title)
        self.setWindowIcon(QIcon(icon_path))
        self.setGeometry(100, 100, *dimensions)
        self.setMinimumSize(800, 600)
        self.stackWidget = QStackedWidget()
        self.init_ui()

    
    def init_ui(self):
        drag_drop_element = DragDropElement()
        display_data_element = DisplayDataElement()
        centered_drag = self.make_centered_widget(drag_drop_element)
        centered_display = self.make_centered_widget(display_data_element)
        self.stackWidget.addWidget(centered_drag)
        self.stackWidget.addWidget(centered_display)
        self.stackWidget.setCurrentIndex(0)
        container = QWidget(self)
        hbox = QHBoxLayout(container)
        hbox.setAlignment(Qt.AlignmentFlag.AlignCenter)
        hbox.addWidget(self.stackWidget)
        container.setLayout(hbox)
        drag_drop_element.signal.connect(lambda data: self._on_file_dropped(data, display_data_element))
        self.setCentralWidget(container)
    

    def _on_file_dropped(self,data, display_element: DisplayDataElement):
        self.stackWidget.setCurrentIndex(1)
        display_element.show_data(data)


    def make_centered_widget(self,inner_widget: QWidget) -> QWidget:
        wrapper = QWidget()
        v_layout = QVBoxLayout(wrapper)
        v_layout.addStretch()  # espace au-dessus
        h_layout = QHBoxLayout()
        h_layout.addStretch()  # espace à gauche
        h_layout.addWidget(inner_widget)
        h_layout.addStretch()  # espace à droite
        v_layout.addLayout(h_layout)
        v_layout.addStretch()  # espace en dessous
        return wrapper
      
        
        
        





        