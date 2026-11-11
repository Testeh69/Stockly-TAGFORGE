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
        
        if fixed_size.width() <=100 or fixed_size.height() <=100:
            self.container.setFixedSize(fixed_size.width()-5, fixed_size.height()-5)
              # Texte
            self.label_text = QLabel(
                        ' <a href="#">ici</a>', 
                        self.container
                        )
            
        else:
            self.container.setFixedSize(fixed_size.width()-20, fixed_size.height()-20)
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
        
                # --- Palette ---
        is_compact = fixed_size.width() <= 100 or fixed_size.height() <= 100

        if is_dark_mode:
            background = "#172033"
            border = "#293750"
            accent = "#64E9EE"
            text_color = "#EAF2FA"
            hover_background = "#24344D"
        else:
            background = "#F4F7FC"
            border = "#DCE4EF"
            accent = "#0078D7"
            text_color = "#243247"
            hover_background = "#E5F0FC"

        # --- Layout principal ---
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # --- Conteneur ---
        self.container = QWidget(self)
        self.container.setObjectName("dropContainer")

        if is_compact:
            self.container.setFixedSize(
                fixed_size.width() - 5,
                fixed_size.height() - 5
            )
            label_text = '<a href="#">IMPORTER</a>'
            icon_size = QSize(45, 45)
            font_size = 8
        else:
            self.container.setFixedSize(
                fixed_size.width() - 20,
                fixed_size.height() - 20
            )
            label_text = 'Déposez votre fichier Excel <a href="#">ici</a>'
            icon_size = QSize(100, 100)
            font_size = 10

        # --- Style ---
        self.container.setStyleSheet(f"""
            QWidget#dropContainer {{
                background-color: {background};
                border: 1px solid {border};
                border-radius: 10px;
            }}

            QWidget#dropContainer:hover {{
                background-color: {hover_background};
                border: 1.5px solid {accent};
            }}
        """)

        # --- Ombre ---
        shadow = QGraphicsDropShadowEffect(self.container)
        shadow.setBlurRadius(12 if is_compact else 15)
        shadow.setXOffset(0)
        shadow.setYOffset(3)
        shadow.setColor(QColor(accent))
        self.container.setGraphicsEffect(shadow)

        # --- Layout interne ---
        inner_layout = QVBoxLayout(self.container)
        inner_layout.setContentsMargins(4, 4, 4, 4)
        inner_layout.setSpacing(4)
        inner_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # --- Icône ---
        self.label_icon = QLabel(self.container)
        self.label_icon.setPixmap(
            QIcon(icon_path).pixmap(icon_size)
        )
        self.label_icon.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # --- Texte ---
        self.label_text = QLabel(label_text, self.container)
        self.label_text.setFont(QFont("Segoe UI", font_size, QFont.Weight.DemiBold))
        self.label_text.setStyleSheet(f"""
            QLabel {{
                color: {text_color};
                background: transparent;
                border: none;
            }}
            QLabel a {{
                color: {accent};
                text-decoration: none;
                font-weight: bold;
            }}
        """)

        self.label_text.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.label_text.setOpenExternalLinks(False)
        self.label_text.linkActivated.connect(
            self._acces_file_from_desktop
        )

        # --- Assemblage ---
        inner_layout.addWidget(self.label_icon)
        inner_layout.addWidget(self.label_text)

        main_layout.addWidget(self.container)

    def dragEnterEvent(self, event):
        if event.mimeData().hasUrls():
            event.accept()
        else:
            event.ignore()

    def dropEvent(self, event):
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
            self.load_excel_file(file_path)
            if self.imported_dataframe is not None:
                self.data_ready.emit(self.imported_dataframe)
        
    def _normalize_column_name(self,name: str) -> str:
        """Normalise un nom de colonne : minuscules + suppression des accents + suppression des espaces inutiles"""
        name = str(name).strip().lower()
        name = unicodedata.normalize('NFKD', name).encode('ASCII', 'ignore').decode('ASCII')
        name = name.replace(' ', '_')
        return name

    def load_excel_file(self, file_path):
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
        