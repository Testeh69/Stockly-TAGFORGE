import PyInstaller.__main__
"""
Building script for StocklyTagForge application using PyInstaller.
This script configures PyInstaller to package the application into a single executable file,
including necessary data directories and setting application properties.
"""


PyInstaller.__main__.run([
    'main.py',
    # '--console',                       # affiche la console noire
    '--name=StocklyTagForge',          # nom de l'exécutable
    '--onefile',                       # un seul fichier exe
    '--clean',                         # nettoie le cache PyInstaller
    '--noconfirm',                     # écrase l'ancien build sans demander
    '--add-data=ui;ui',                # inclure dossier ui
    '--add-data=core;core',            # inclure dossier core
    '--add-data=assets;assets',        # inclure dossier assets
    '--icon=assets/icon.ico',           # icône de l'application
    '--hidden-import=openpyxl',
    '--windowed'                       # ⚡ supprime la console noire
])