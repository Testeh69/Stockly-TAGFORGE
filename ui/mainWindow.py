from PyQt6.QtWidgets import QMainWindow, QWidget, QVBoxLayout, QStackedWidget
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
        self.stack_widget = QStackedWidget(self)
        self.file = None
        self.drag_drop_element = None
        self.display_data_element = None
        self.setWindowTitle(title)
        self.setGeometry(100, 100, dimensions[0], dimensions[1])
        self.setMinimumSize(500, 200)   
        self.setWindowIcon(QIcon(icon_path))
        self._setup_main_ui()



    def _setup_main_ui(self):
        """Set up the main UI components."""
        central_widget = QWidget(self)
        layout = QVBoxLayout()
        self.drag_drop_element = DragDropElement()
        self.display_data_element = DisplayDataElement()
        self.stack_widget.addWidget(self.drag_drop_element)
        self.stack_widget.addWidget(self.display_data_element)
        self.drag_drop_element.data.connect(self.display_table)
        layout.addWidget(self.stack_widget, alignment=Qt.AlignmentFlag.AlignCenter)
        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)

    
    def display_table(self, data):
        """
        Display the data in the display_data_element.
        """
        self.display_data_element.show_data(data)
        self.stack_widget.setCurrentWidget(self.display_data_element)
        