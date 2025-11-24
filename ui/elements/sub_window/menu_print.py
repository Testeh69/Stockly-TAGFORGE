from core.utils import generate_zpl
from core.qr_system import QRCodeGenerator



from PIL import Image
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QMessageBox,QDialog,QPushButton,QLabel, QComboBox,QVBoxLayout,QHBoxLayout, QToolButton
from PyQt6.QtGui import QIcon
from PyQt6.QtCore import QSize
import win32print
import win32ui



class MenuPrint(QDialog):
    def __init__(self, parent=None, data_to_print = None):
        super().__init__(parent)
        self.data_to_print = data_to_print
        self.setWindowTitle("Menu d'impression")
        self.setWindowIcon(QIcon("assets/logo.png"))
        self.setFixedSize(600, 500)
        self.setWindowModality(Qt.WindowModality.ApplicationModal)
        layout = QHBoxLayout()

        btn_classic = UIBtnPrinter(
            title="Imprimante Classique",
            func=print_classic,
            data_to_print=self.data_to_print
        )

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


    def __init__(self, parent=None, icon_path:str="assets/print.svg", size:int=150, title: str = "Imprimante Classique",size_ui = (250,325), func = None, data_to_print = None  ):
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







def print_zebra(data_to_print, parent=None):
    if not data_to_print:
        print("Aucune donnée à imprimer.")
        return

    printer_name = "ZDesigner ZT230-200dpi ZPL"  # Nom exact de ton imprimante

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

def print_classic(data_list, parent=None):
    if not data_list:
        print("Aucune donnée à imprimer.")
        return

    # Afficher le menu de sélection
    dialog = PrinterSelectionDialog(parent)
    if dialog.exec() != QDialog.DialogCode.Accepted:
        return  # utilisateur a annulé

    printer_name = dialog.get_selected_printer()

    # Essayer de se connecter à l'imprimante
    try:
        hPrinter = win32print.OpenPrinter(printer_name)
    except Exception as e:
        print(f"Erreur de connexion à l'imprimante : {e}")
        if parent:
            QMessageBox.warning(parent, "Erreur Imprimante",
                                f"Impossible de se connecter à l'imprimante {printer_name}.")
        return

    try:
        hDC = win32ui.CreateDC()
        hDC.CreatePrinterDC(printer_name)
        hDC.StartDoc("Print QR + Text")
        hDC.StartPage()

        y_offset = 0

        for data in data_list:
            # Générer QR code
            data_text = f"Designation:{data['designation']}, Reference:{data['reference']}"
            if data.get("lot") == "nan":
                data_text += ", Lot: N/A"
            else:
                data_text += f", Lot:{data['lot']}"

            qr_path = QRCodeGenerator.generate_qr_code(data_text)
            qr_img = Image.open(qr_path)

            # Afficher QR code
            hDC.DrawBitmap(qr_img, (100, y_offset))
            y_offset += qr_img.height + 20

            # Afficher texte
            hDC.TextOut(100, y_offset, data_text)
            y_offset += 100

        hDC.EndPage()
        hDC.EndDoc()
        hDC.DeleteDC()

    except Exception as e:
        print(f"Erreur pendant l'impression : {e}")
        if parent:
            QMessageBox.warning(parent, "Erreur Impression",
                                f"Une erreur est survenue pendant l'impression : {e}")

    finally:
        try:
            win32print.ClosePrinter(hPrinter)
        except:
            pass  # même si la fermeture échoue, on ignore




class PrinterSelectionDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Sélectionner une imprimante")
        self.setFixedSize(400, 150)
        self.setWindowModality(Qt.WindowModality.ApplicationModal)

        layout = QVBoxLayout(self)
        layout.addWidget(QLabel("Choisissez une imprimante :"))

        self.combo = QComboBox()
        self.printers = [printer[2] for printer in win32print.EnumPrinters(
            win32print.PRINTER_ENUM_LOCAL | win32print.PRINTER_ENUM_CONNECTIONS)]
        self.combo.addItems(self.printers)
        layout.addWidget(self.combo)

        btn_ok = QPushButton("Valider")
        btn_ok.clicked.connect(self.accept)
        layout.addWidget(btn_ok)

    def get_selected_printer(self):
        return self.combo.currentText()