from PyQt6.QtWidgets import QApplication
from PyQt6.QtGui import QPalette
from PyQt6.QtPrintSupport import QPrinter
from PIL import Image
import win32ui
import win32con
import unicodedata


def normalize_column_name(
        name: str
        ) -> str:
    
    """Normalise un nom de colonne : minuscules + suppression des accents + suppression des espaces inutiles"""

    name = str(name).strip().lower()
    name = unicodedata.normalize('NFKD', name).encode('ASCII', 'ignore').decode('ASCII')
    return name


def convert_mm_to_px(
        mm:float, 
        printer:QPrinter
        )->int:
    
    """Convertit des millimètres en pixels selon la résolution de l'imprimante."""

    dpi = printer.resolution()
    inches = mm / 25.4
    pixels = int(inches * dpi)
    return pixels


def convert_pil_to_win32_bitmap(
        pil_image: Image.Image
        )-> win32ui.CreateBitmap:
    
    """Convertit une image PIL en bitmap Windows compatible PyCDC."""

    dib = Image.frombytes("RGB", pil_image.size, pil_image.tobytes(), "raw", "RGB")
    # On convertit en DIB Windows
    bmp = win32ui.CreateBitmap()
    bmp.CreateCompatibleBitmap(win32ui.CreateDC(), pil_image.width, pil_image.height)
    hdc = win32ui.CreateDC()
    hdc.CreateCompatibleDC()
    old = hdc.SelectObject(bmp)
    hdc.BitBlt((0, 0), pil_image.size, dib, (0, 0), win32con.SRCCOPY)
    hdc.SelectObject(old)
    hdc.DeleteDC()
    return bmp


def detect_dark_mode()->bool:

    """Détecte si l'application est en mode sombre ou clair"""

    palette = QApplication.palette()
    window_color = palette.color(QPalette.ColorRole.Window)
    is_dark = window_color.value() < 128
    return is_dark




def generate_zpl(
        data_text: str
        ) -> str:
    
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