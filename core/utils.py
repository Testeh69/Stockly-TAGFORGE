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