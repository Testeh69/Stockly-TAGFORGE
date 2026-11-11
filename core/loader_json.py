import json
from typing import Any


class ConfigManager:
    """
    A class to manage configuration settings loaded from a JSON file, 
    allowing for easy access to nested keys.

    """
    def __init__(self, path_file: str):
        self.path_file = path_file
        self._data = self._load()

    def _load(self) -> dict:
        with open(self.path_file, "r", encoding="utf-8") as file:
            return json.load(file)


    def write(self,key,new_data):
        """
        Write a new value to a specific key in the configuration and save it back to the JSON file.
        """
        keys = key.split(".")
        data = self._data

        for k in keys[:-1]:
            if k not in data or not isinstance(data[k], dict):
                data[k] = {}
            data = data[k]

        data[keys[-1]] = new_data

        with open(self.path_file, "w", encoding="utf-8") as file:
            json.dump(self._data, file, indent=4)

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