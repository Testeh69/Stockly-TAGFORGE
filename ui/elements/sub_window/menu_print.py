from core.utils import generate_zpl
from core.qr_system import QRCodeGenerator
from PIL import Image
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QMessageBox,QDialog,QPushButton,QLabel, QComboBox,QVBoxLayout,QHBoxLayout, QToolButton
from PyQt6.QtGui import QIcon,QImage, QPainter
from PyQt6.QtPrintSupport import QPrinter, QPrintDialog
from PyQt6.QtCore import QSize
import win32print



"""Menu d'impression pour choisir le type d'imprimante et lancer l'impression."""

class MenuPrint(QDialog):
    def __init__(self, parent=None, data_to_print: list[dict[str,str]] = None):
        super().__init__(parent)
        self.data_to_print = data_to_print
        self.setWindowTitle("Menu d'impression")
        self.setWindowIcon(QIcon("assets/logo.png"))
        self.setFixedSize(600, 500)
        self.setWindowModality(Qt.WindowModality.ApplicationModal)
        layout = QHBoxLayout()


        """Bouton pour l'imprimante classique"""
        btn_classic = UIBtnPrinter(
            title="Imprimante Classique",
            func=print_classic,
            data_to_print=self.data_to_print
        )
        """Bouton pour l'imprimante Zebra"""
        btn_zebra = UIBtnPrinter(
            title="Imprimante Zebra",
            icon_path="assets/zebra_printer.svg",
            func=print_zebra,
            data_to_print=self.data_to_print
        )

        # Ajouter les boutons au layout
        layout.addWidget(btn_classic)
        layout.addWidget(btn_zebra)
        self.setLayout(layout)  
        

    def close(self):
        super().close()




class UIBtnPrinter(QToolButton):

    """ Bouton pour les différents types d'imprimantes (Classique et Zebra)"""


    def __init__(self, 
                 parent=None, 
                 icon_path:str="assets/print.svg", 
                 size:int=150, 
                 title: str = "Imprimante Classique",
                 size_ui = (250,325), 
                 func = None, 
                 data_to_print:list[dict[str,str]] = None
                ):
        """Initialisation du bouton d'imprimante.
        args:
            parent: QWidget parent du bouton.
            icon_path: Chemin de l'icône du bouton.
            size: Taille de l'icône.
            title: Titre du bouton.
            size_ui: Taille du bouton.
            func: Fonction d'impression associée au bouton, (elles doivent toujours reçevoirent un argument (pd.Dataframe)).
            data_to_print: Données à imprimer.
        """
        super().__init__( parent)
        self.setIcon(QIcon(f"{icon_path}"))
        self.setIconSize(QSize(size, size))
        self.setFixedSize(size_ui[0], size_ui[1])
        self.setText(title)
        self.func = func
        self.setToolButtonStyle(Qt.ToolButtonStyle.ToolButtonTextUnderIcon)
        self.clicked.connect(self.on_click)
        self.data_to_print = data_to_print

    def on_click(self):
        if callable(self.func):
            self.func(self.data_to_print)
        else:
            print("Fonction d'impression non définie.")





""" Fonction d'impression pour les imprimantes Zebra."""

def print_zebra(data_to_print:list[dict[str,str]], parent=None):
    if not data_to_print:
        print("Aucune donnée à imprimer.")
        return

    printer_name:str = "ZDesigner ZT230-200dpi ZPL"  # Nom exact de ton imprimante

    # Essayer de se connecter à l'imprimante
    try:
        hPrinter = win32print.OpenPrinter(printer_name)
    except Exception as e:
        print(f"Erreur de connexion à l'imprimante Zebra : {e}")
        if parent:
            QMessageBox.warning(parent, "Erreur Imprimante",
                                f"Impossible de se connecter à l'imprimante Zebra ({printer_name}).")
        return  # on sort simplement de la fonction, pas de crash

    try:
        hJob = win32print.StartDocPrinter(hPrinter, 1, ("Label Print", None, "RAW"))
        win32print.StartPagePrinter(hPrinter)

        for data in data_to_print:
            data_text = f"Designation:{data['designation']}, Reference:{data['reference']}"
            if data.get("lot") == "nan":
                data_text += ", Lot: N/A"
            else:
                data_text += f", Lot:{data['lot']}"

            zpl_command = generate_zpl(data_text)
            win32print.WritePrinter(hPrinter, zpl_command.encode("utf-8"))

        win32print.EndPagePrinter(hPrinter)
        win32print.EndDocPrinter(hPrinter)

    except Exception as e:
        print(f"Erreur pendant l'impression Zebra : {e}")
        if parent:
            QMessageBox.warning(parent, "Erreur Impression",
                                f"Une erreur est survenue pendant l'impression Zebra : {e}")

    finally:
        try:
            win32print.ClosePrinter(hPrinter)
        except:
            pass



def print_classic(
        data_list:list[dict[str,str]], 
        parent=None
        ):
    """Fonction d'impression pour les imprimantes classiques."""
    
    if not data_list:
        print("Aucune donnée à imprimer.")
        return
    # Création de la boite de dialogue pour sélectionner l'imprimante
    dialog = PrinterSelectionDialog(parent)
    if dialog.exec() == QDialog.DialogCode.Accepted:
        printer_name:str = dialog.get_selected_printer()
        printer = QPrinter()
        printer.setPrinterName(printer_name)
        painter_qt = QPainter(printer)
        data_list = QRCodeGenerator.convert_data_to_specific_format(data_list)
        bank_link_picutures = []
        for data in data_list:
            link_pictures = QRCodeGenerator.generate_qr_code(data)
            bank_link_picutures.append(link_pictures)
            painter_qt.drawImage(0, 0, QImage(link_pictures))
            painter_qt.end()    
        for link in bank_link_picutures:
            QRCodeGenerator.delete_qr_code(link)
        return
    else:
        return  # L'utilisateur a annulé la sélection
    


class PrinterSelectionDialog(QDialog):

    """Boîte de dialogue pour sélectionner une imprimante classique disponible sur le réseaux."""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Sélectionner une imprimante")
        self.setFixedSize(400, 150)
        self.setWindowModality(Qt.WindowModality.ApplicationModal)

        layout = QVBoxLayout(self)
        layout.addWidget(QLabel("Choisissez une imprimante :"))

        self.combo = QComboBox()
        #Liste des imprimantes disponibles sur le réseau local et en connexion
        self.printers = [printer[2] for printer in win32print.EnumPrinters(
            win32print.PRINTER_ENUM_LOCAL | win32print.PRINTER_ENUM_CONNECTIONS)]
        self.combo.addItems(self.printers)
        layout.addWidget(self.combo)

        btn_ok = QPushButton("Valider")
        btn_ok.clicked.connect(self.accept)
        layout.addWidget(btn_ok)

    def get_selected_printer(self)-> str:
        return self.combo.currentText()
    