import json
from typing import Any


class JSONLoader:
    """Classe pour charger et lire des fichiers JSON avec accès profond."""

    def __init__(self, path_file: str):
        self.path_file = path_file
        self._data = self._load()

    def _load(self) -> dict:
        with open(self.path_file, "r", encoding="utf-8") as file:
            return json.load(file)

    def get(self, key_path: str, default: Any = None) -> Any:
        """
        Accède à une clé JSON de profondeur arbitraire.
        Exemple : "offset.qr.x_mm"
        """
        keys = key_path.split(".")
        value = self._data

        for key in keys:
            if isinstance(value, dict) and key in value:
                value = value[key]
            else:
                return default

        return value