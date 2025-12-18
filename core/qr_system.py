import qrcode
import json
import uuid
import os

class QRCodeGenerator:
    """
    Classe pour générer des QR codes à partir de données JSON, manipuler.
    """
    @staticmethod
    def convert_data_to_specific_format(
            data:dict[str,str]
        ) -> dict[str,str]:
        
        """Convertit les données au format spécifique attendu pour le QR code dans generate8QR_Code."""
        
        list_data = []
        for sp_data in data:
            data_text = f"Designation:{sp_data['designation']}, Reference:{sp_data['reference']}"
            if sp_data.get("lot") == "nan":
                data_text += ", Lot: N/A"
            else:
                data_text += f", Lot:{sp_data['lot']}"
            list_data.append(data_text)
        return list_data
    
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
            box_size=5,
            border=2,
        )
        qr.add_data(json_data)
        qr.make(fit=True)
        img = qr.make_image(fill_color="black", back_color="white")
        img.save(path_output)
        return path_output

    @staticmethod
    def delete_qr_code(path_file:str):
        """Supprime le fichier QR code généré."""
        if os.path.exists(path_file):
            os.remove(path_file)
            return True
        return False



