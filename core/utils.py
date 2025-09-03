import unicodedata


def normalize_column_name(name: str) -> str:
    """Normalise un nom de colonne : minuscules + suppression des accents + suppression des espaces inutiles"""
    name = str(name).strip().lower()
    name = unicodedata.normalize('NFKD', name).encode('ASCII', 'ignore').decode('ASCII')
    return name
