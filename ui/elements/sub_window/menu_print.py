from core.utils import generate_zpl, convert_mm_to_px
from core.qr_system import QRCodeGenerator
from core.loader_json import JSONLoader
from PIL import Image
from PyQt6.QtCore import Qt, QRect
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
    # Chargement de la configuration d'impression
    cfg = JSONLoader("config/print_classic.json")
    
    # Récupération des paramètres d'impression
    qr_size:int = cfg.get("qr.size_mm")
    font_size :int = cfg.get("font.size_pt")
    bloc_text_height:int = cfg.get("offset.text.height_mm")
    bloc_text_width:int = cfg.get("offset.text.width_mm")
    offset_qr:dict[str,str] = cfg.get("offset.qr")
    offset_text:dict[str,str] = cfg.get("offset.text")
    num_qr_printed:int = cfg.get("stats.nb_qr_printed_file")


    # Création de la boite de dialogue pour sélectionner l'imprimante
    dialog = PrinterSelectionDialog(parent)
    if dialog.exec() == QDialog.DialogCode.Accepted:
        printer_name:str = dialog.get_selected_printer()
        printer = QPrinter()
        printer.setPrinterName(printer_name)
        
        
        painter_qt = QPainter(printer)
        
        # Conversion des tailles en mm vers pixels
        #Par défaut les unités de QPrinter sont en pixels
        qr_size:int = convert_mm_to_px(qr_size, printer)
        offset_qr_x:int = convert_mm_to_px(offset_qr['x_mm'], printer)
        offset_qr_y:int = convert_mm_to_px(offset_qr['y_mm'], printer)
        offset_text_x:int = convert_mm_to_px(offset_text['x_mm'], printer)
        offset_text_y:int = convert_mm_to_px(offset_text['y_mm'], printer)
        text_height:int = convert_mm_to_px(bloc_text_height, printer)
        text_width:int = convert_mm_to_px(bloc_text_width, printer)

        # Position de départ pour dessiner les QR codes
        x:int = offset_qr_x
        y:int = offset_qr_y
        
        formated_data_list = QRCodeGenerator.convert_data_to_specific_format(data_list)
        temporary_files = []
        
        # Boucle qui gère la position d'impression de chaque QR code et son texte associé
        for data in zip(formated_data_list, data_list):
            link_pictures = QRCodeGenerator.generate_qr_code(data[0])
            temporary_files.append(link_pictures)
            
          
            image = QImage(link_pictures).scaled(
                qr_size,
                qr_size,
                Qt.AspectRatioMode.KeepAspectRatio,
                Qt.TransformationMode.SmoothTransformation
            )

            painter_qt.drawImage(
                x,
                y,
                image
            )
            
            if len(data[1]["designation"]) > 15:
                data[1]["designation"] = data[1]["designation"][:12] + "..."
            if len(data[1]["reference"]) > 15:
                data[1]["reference"] = data[1]["reference"][:7] + "..." + data[1]["reference"][-4:]
            if len(data[1]["lot"])>15:
                data_lot_of = data[1]["lot"].split("CC")[0]
                data_lot_cc = "CC"+data[1]["lot"].split("CC")[-1].split("TS")[0]
                data_lot_ts = "TS"+data[1]["lot"].split("TS")[0]
            
            if len(data_lot_ts) >= 10:
                truncated_ts = f"{data_lot_ts[:3]}...{data_lot_ts[-4:]}" if len(data_lot_ts) >= 7 else data_lot_ts
            else:
                truncated_ts = data_lot_ts
            
            text_tag = f"{data[1]['designation']}\n{data[1]['reference']}"
          
            text_lot = f"Lot:{data_lot_of}\n{data_lot_cc}\n{truncated_ts}"

            #Texte de la désignation + référence
            text_tag_rect = QRect(
                x,
                y + qr_size + offset_text_y,
                text_width,
                text_height
            )
            painter_qt.drawText(
                text_tag_rect,
                Qt.AlignmentFlag.AlignLeft | Qt.TextFlag.TextWordWrap,
                text_tag
            )


            #Texte du lot
            text_lot_rect = QRect(
                x,
                y + qr_size + text_height/2 +  2*offset_text_y + 5,
                text_width,
                text_height
            )

            painter_qt.drawText(
                text_lot_rect,
                Qt.AlignmentFlag.AlignLeft | Qt.TextFlag.TextWordWrap,
                text_lot
            )

            num_qr_printed += 1
            if num_qr_printed % 5 == 0:
                x = offset_qr_x  # Réinitialise x à la marge de gauche
                y += qr_size + offset_qr_y + text_height +2*offset_text_y  # Avance y pour la nouvelle ligne            
            else:
                x += qr_size + offset_text_x  # Avance x pour le prochain QR code

        #hors boucle pour éviter d'ouvrir et fermer plusieurs fois l'imprimante
        painter_qt.end()    
        for link in temporary_files:
            #suppression des images temporaires après impression
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
    