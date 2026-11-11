import os 
import pandas as pd
import unicodedata
from PyQt6.QtWidgets import QWidget, QVBoxLayout,QFileDialog, QLabel, QGraphicsDropShadowEffect
from PyQt6.QtGui import QFont, QIcon, QColor
from PyQt6.QtCore import Qt, pyqtSignal, QSize, QStandardPaths
from core.utils import detect_dark_mode


           



class FileUploader(QWidget):

    data_ready = pyqtSignal(pd.DataFrame)
    error_occurred = pyqtSignal(str)

    def __init__(self, parent=None, fixed_size:QSize=QSize(220, 220)):
        super().__init__(parent)
        self.imported_dataframe = None

        self.setAcceptDrops(True)
        self.setFixedSize(fixed_size)

        is_dark_mode = detect_dark_mode()

        text_color = "#FFFFFF" if is_dark_mode else "#000000"
        icon_path = "assets/file.svg" 

        # Layout principal
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # Conteneur stylé
        self.container = QWidget(self)
        self.container.setObjectName("dropContainer")
        if fixed_size.width() > 20 and fixed_size.height() > 20:
            self.container.setFixedSize(fixed_size.width()-5, fixed_size.height()-5)
        else:
            self.container.setFixedSize(fixed_size.width()-20, fixed_size.height()-20)

        bg_color = "rgba(10, 10, 10, 0.2)" if is_dark_mode else "rgba(240, 240, 240, 0.8)"
        border_color = "#64E9EE" if is_dark_mode else "#0078D7"

        # Appliquer au conteneur
        self.container.setStyleSheet(f"""
            QWidget#dropContainer {{
                background-color: {bg_color};
                border: 1.5px solid {border_color};
                border-radius: 10px;
            }}
        """)

        # Ombre portée
        shadow = QGraphicsDropShadowEffect(self.container)
        shadow.setBlurRadius(15)
        shadow.setXOffset(3)
        shadow.setYOffset(3)
        shadow.setColor(QColor("#64E9EE"))
        self.container.setGraphicsEffect(shadow)

        # Layout interne
        inner_layout = QVBoxLayout(self.container)
        inner_layout.setContentsMargins(6, 6, 6, 6)
        inner_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # Icône
        self.label_icon = QLabel(self.container)
        self.label_icon.setPixmap(QIcon(icon_path).pixmap(QSize(100, 100)))
        self.label_icon.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # Texte
        self.label_text = QLabel(
            'Déposez votre fichier Excel <a href="#">ici</a>', 
            self.container
            )
        self.label_text.setFont(QFont("Segoe UI", 10))
        self.label_text.setStyleSheet(f"color: {text_color};")
        self.label_text.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.label_text.setOpenExternalLinks(False)
        self.label_text.linkActivated.connect(self._acces_file_from_desktop)

        # Ajouter au layout interne
        inner_layout.addWidget(self.label_icon)
        inner_layout.addWidget(self.label_text)

        # Ajouter le conteneur au layout principal
        main_layout.addWidget(self.container)

    def _dragEnterEvent(self, event):
        if event.mimeData().hasUrls():
            event.accept()
        else:
            event.ignore()

    def _dropEvent(self, event):
        # Access the file path from the dropped item
        urls = event.mimeData().urls()
        #print(urls)
        if not urls:
            return 
        path = urls[0].toLocalFile()
        if path.endswith('.xlsx'):
            self.load_excel_file(path)
            #print("File loaded successfully:", path)
            self.data_ready.emit(self.imported_dataframe)
       
          
    def _acces_file_from_desktop(self):
        """Ouvre une boîte de dialogue pour sélectionner un fichier Excel depuis le bureau."""
        file_path, _ = QFileDialog.getOpenFileName(
            self,
            "Choisir un fichier Excel",
            QStandardPaths.writableLocation(QStandardPaths.StandardLocation.DesktopLocation),
            "Excel Files (*.xlsx *.xls)"
        )
        if file_path:
            self._load_excel_file(file_path)
            if self.imported_dataframe is not None:
                self.data_ready.emit(self.imported_dataframe)
        
    def _normalize_column_name(self,name: str) -> str:
        """Normalise un nom de colonne : minuscules + suppression des accents + suppression des espaces inutiles"""
        name = str(name).strip().lower()
        name = unicodedata.normalize('NFKD', name).encode('ASCII', 'ignore').decode('ASCII')
        name = name.replace(' ', '_')
        return name

    def _load_excel_file(self, file_path):
        '''
        Charge un fichier Excel, normalise les noms de colonnes 
        et extrait les colonnes "reference", "n_lot" et "designation" 
        pour les stocker dans self.imported_dataframe.
        '''
        if not os.path.exists(file_path):
            return None
        try:
            df = pd.read_excel(file_path)
            df.columns = [self._normalize_column_name(col) for col in df.columns]
            print("Colonnes normalisées :", df.columns.tolist())
            self.imported_dataframe = df[["reference","n_lot","designation"]]
            self.imported_dataframe.columns = ["référence", "lot", "designation"]
        except Exception as e:
            print(f"Error loading Excel file: {e}")
            return None

    def load_and_emit(self, file_path):
        """Charge un fichier Excel et émet le signal data_ready avec le DataFrame résultant."""
        self._load_excel_file(file_path)
        if self.imported_dataframe is not None:
            self.data_ready.emit(self.imported_dataframe)

    def _show_data(self):
        print(self.imported_dataframe)
        