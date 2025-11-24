import unicodedata
from PyQt6.QtWidgets import QApplication
from PyQt6.QtGui import QPalette

def normalize_column_name(name: str) -> str:
    """Normalise un nom de colonne : minuscules + suppression des accents + suppression des espaces inutiles"""
    name = str(name).strip().lower()
    name = unicodedata.normalize('NFKD', name).encode('ASCII', 'ignore').decode('ASCII')
    return name



def detect_dark_mode()->bool:
    """Détecte si l'application est en mode sombre ou clair"""
    palette = QApplication.palette()
    window_color = palette.color(QPalette.ColorRole.Window)
    is_dark = window_color.value() < 128
    return is_dark




def generate_zpl(data_text: str) -> str:
    """
    Génère le ZPL centré pour un QR code + texte.
    Ajuste les positions X,Y selon ton étiquette.
    pour les imprimantes zebra
    """
    zpl = f"""^XA
        ^FO170,25
        ^BQN,2,4
        ^FDLA,{data_text}^FS
        ^FO100,220
        ^A0N,14,14
        ^FB400,3,0,C,0
        ^FD{data_text}^FS
        ^XZ
        """
    return zpl