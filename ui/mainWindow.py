import os
from pathlib import Path
import pandas as pd


from PyQt6.QtWidgets import QMainWindow, QVBoxLayout,QWidget,QHBoxLayout , QStackedWidget
from PyQt6.QtGui import QIcon
from PyQt6.QtCore import Qt
from core.loader_json import ConfigManager
from ui.elements.file_uploader import FileUploader 
from ui.elements.display_data import DisplayDataElement

class StockTagForgeMainWindow(QMainWindow):
    """Main window for the Stockly TagForge application, handling the main interface and navigation between different views."""
    def __init__(self, title:str = "STOCKLY TAGFORGE", icon_path:str = "assets/logo.png", dimensions:list[int] = (1000, 800)):
        """
        Initialize the main window with a title, icon, and dimensions.
        """
        super().__init__()


        self.config = ConfigManager("config/settings.json")
        self.path = None

        self.setWindowTitle(title)
        self.setWindowIcon(QIcon(icon_path))
        self.setGeometry(100, 100, *dimensions)
        self.setMinimumSize(800, 600)
        self.stackWidget = QStackedWidget()
        self.name_file = None
        self.init_ui()

    
    def init_ui(self):
        """
        Initialize the user interface, setting up the file uploader and display elements, and handling file drop events.
        """
        self.file_uploader_element = FileUploader()
        self.display_data_element = DisplayDataElement()
        centered_file_uploader = self.make_centered_widget(self.file_uploader_element)
        centered_display = self.make_centered_widget(self.display_data_element)
        self.stackWidget.addWidget(centered_file_uploader)
        self.stackWidget.addWidget(centered_display)
        self.stackWidget.setCurrentIndex(0)
        container = QWidget(self)
        hbox = QHBoxLayout(container)
        hbox.setAlignment(Qt.AlignmentFlag.AlignCenter)
        hbox.addWidget(self.stackWidget)
        container.setLayout(hbox)
        print(self._check_is_file_on_desktop())

        self.file_uploader_element.data_ready.connect(
            self._on_file_ready
        )

        if self._check_is_file_on_desktop():
            try:
                self.file_uploader_element.load_and_emit(self.path)
            except Exception as e:
                print(f"Error loading Excel file: {e}")

        self.file_uploader_element.data_ready.connect(lambda data: self._on_file_dropped(data, self.display_data_element))
        self.setCentralWidget(container)
    

    def _on_file_ready(self, data):
        """
        Handle the event when data is ready from the file uploader, updating the display element with the new data and switching to the display view.
        """
        self.stackWidget.setCurrentIndex(1)
        self.display_data_element.show_data(data)

    def _on_file_dropped(self,data, display_element: DisplayDataElement):
        """
        Handle the event when a file is dropped, updating the display element with the new data and switching to the display view.
        """
        self.stackWidget.setCurrentIndex(1)
        display_element.show_data(data)




    def _check_is_file_on_desktop(self) -> bool:
        """
        Find the most recent stock file in the configured folder.
        """

        possible_path = self.config.get(
            "default_file_access.path_to_access_default_name_stock_file"
        )

        folder = Path(possible_path)
        allowed_extensions = [".xlsx", ".xls"]

        matching_files = []

        for file in folder.iterdir():
            if (
                file.is_file()
                and file.suffix.lower() in allowed_extensions
                and file.name.lower().startswith("inventaire du")
            ):
                matching_files.append(file)
                self.config.write(
                    "default_file_access.debug_last_checked_file",
                    True
                )


        if not matching_files:
            self.config.write(
                "default_file_access.debug_is_file_on_desktop",
                False
            )
            return False

        latest_file = max(
            matching_files,
            key=lambda f: f.stat().st_mtime
        )

        self.path =  str(latest_file)
        self.config.write(
            "default_file_access.debug_is_file_on_desktop",
            True
        )

        return True

    def make_centered_widget(self,inner_widget: QWidget) -> QWidget:
        """
        Create a wrapper widget that centers the given inner widget both horizontally and vertically, adding stretchable space around it for proper alignment.
        """
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
      
        
        
        





        