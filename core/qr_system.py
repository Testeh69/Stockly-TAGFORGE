import qrcode
import json
import uuid
import os

class QRCodeGenerator:
    """
    Classe pour générer des QR codes à partir de données JSON.
    """

    @staticmethod
    def generate_qr_code(data:str, path_folder:str  = None):
        if path_folder:
            path_output = os.path.join(path_folder, f"qr_code_{uuid.uuid4()}.png")
        else:
            path_output = f"qr_code_{uuid.uuid4()}.png"
        json_data = json.dumps(data)
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=10,
            border=4,
        )
        qr.add_data(json_data)
        qr.make(fit=True)
        img = qr.make_image(fill_color="black", back_color="white")
        img.save(path_output)
        return path_output





