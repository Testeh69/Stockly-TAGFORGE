from PyQt6.QtWidgets import QPushButton
import tempfile
import win32print
from core.qr_system import QRCodeGenerator

class BtnPrint(QPushButton):

    def __init__(self, label: str = "ALL", parent=None, data_to_print=None):
        super().__init__(label, parent)
        self.data_to_print = data_to_print
        self.clicked.connect(self.on_click)
        self.data_list = None

    def on_click(self):
        if callable(self.data_to_print):
            self.data_list = self.data_to_print()
        else:
            self.data_list = self.data_to_print
        self.print_checked_rows()

    def generate_zpl(self, data_text):
        """
        Génère le ZPL centré pour un QR code + texte.
        Ajuste les positions X,Y selon ton étiquette.
        """
        zpl = f"""
        ^XA
        ^FO100,50
        ^BQN,2,5
        ^FDLA,{data_text}^FS
        ^FO100,200
        ^A0N,30,30
        ^FB400,3,0,C,0
        ^FD{data_text}^FS
        ^XZ
        """
        return zpl

    def print_checked_rows(self):
        if not self.data_list:
            print("⚠ Aucune ligne cochée !")
            return

        printer_name = "Zebra ZT230"  # Nom exact de ton imprimante dans Windows
        hPrinter = win32print.OpenPrinter(printer_name)

        try:
            hJob = win32print.StartDocPrinter(hPrinter, 1, ("Label Print", None, "RAW"))
            win32print.StartPagePrinter(hPrinter)

            for data in self.data_list:
                data_text = f"Lot:{data['lot']}, Designation:{data['designation']}, Reference:{data['reference']}"
                zpl_command = self.generate_zpl(data_text)
                win32print.WritePrinter(hPrinter, zpl_command.encode("utf-8"))

            win32print.EndPagePrinter(hPrinter)
            win32print.EndDocPrinter(hPrinter)
        finally:
            win32print.ClosePrinter(hPrinter)
