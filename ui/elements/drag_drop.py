import os 
import pandas as pd
import unicodedata
from PyQt6.QtWidgets import QWidget, QVBoxLayout,QFileDialog, QLabel, QGraphicsDropShadowEffect
from PyQt6.QtGui import QFont, QIcon, QColor
from PyQt6.QtCore import Qt, pyqtSignal, QSize, QStandardPaths
from core.utils import detect_dark_mode
from core.loader_json import JSONLoader

class DragDropElement(QWidget):

    signal = pyqtSignal(pd.DataFrame, name = "data")

    def __init__(self, parent=None):
        super().__init__(parent)

        self.setAcceptDrops(True)
        self.setFixedSize(220, 220)

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
        self.container.setFixedSize(200, 200)

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
        self.label_text.linkActivated.connect(self.acces_file_from_desktop)

        # Ajouter au layout interne
        inner_layout.addWidget(self.label_icon)
        inner_layout.addWidget(self.label_text)

        # Ajouter le conteneur au layout principal
        main_layout.addWidget(self.container)

    def dragEnterEvent(self, event):
        if event.mimeData().hasUrls():
            event.accept()
        else:
            event.ignore()

    def dropEvent(self, event):
        urls = event.mimeData().urls()
        #print(urls)
        if not urls:
            return 
        path = urls[0].toLocalFile()
        if path.endswith('.xlsx'):
            self.load_excel_file(path)
            self.signal.emit(self.data)
       
            
    def acces_file_from_desktop(self):
        """Ouvre une boîte de dialogue pour sélectionner un fichier Excel depuis le bureau."""
        file_path, _ = QFileDialog.getOpenFileName(
            self,
            "Choisir un fichier Excel",
            QStandardPaths.writableLocation(QStandardPaths.StandardLocation.DesktopLocation),
            "Excel Files (*.xlsx *.xls)"
        )
        if file_path:
            self.load_excel_file(file_path)
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

            # Synonymes attendus
            TARGETS = JSONLoader("config/filter.json")._data


            # Chercher la vraie colonne correspondant à chaque champ cible
            selected_cols = {}
            normalized_map = {self.normalize_column_name(col): col for col in df.columns}
            for target, synonyms in TARGETS.items():
                for syn in synonyms:
                    syn_norm = self.normalize_column_name(syn)
                    if syn_norm in normalized_map:
                        selected_cols[target] = normalized_map[syn_norm]
                        break

            # Vérifier si tout est trouvé
            if len(selected_cols) != 3:
                print("⚠ Colonnes manquantes dans l'Excel ! Trouvées :", selected_cols)
                return None

            # Extraire dans l’ordre souhaité
            self.data = df[[selected_cols["reference"],
                            selected_cols["lot"],
                            selected_cols["designation"]]]

            # Renommer les colonnes
            self.data.columns = ["reference", "lot", "designation"]

            # Filtrer les lignes interdites
            for expr in ["ne pas utiliser", "ne plus utiliser", "non existant"]:
                self.data = self.data[
                    ~self.data.apply(
                        lambda row: row.astype(str).str.lower().str.contains(expr, na=False).any(),
                        axis=1
                    )
                ]

            #self.show_data()
        except Exception as e:
            print(f"Error loading Excel file: {e}")
            return None
        

    def show_data(self):
        print(self.data)
        