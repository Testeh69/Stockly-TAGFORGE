import PyInstaller.__main__

PyInstaller.__main__.run([
    'main.py',
    '--console',                       # affiche la console noire
    '--name=StocklyTagForge',          # nom de l'exécutable
    '--onefile',                       # un seul fichier exe
    '--clean',                         # nettoie le cache PyInstaller
    '--noconfirm',                     # écrase l'ancien build sans demander
    '--add-data=ui;ui',                # inclure dossier ui
    '--add-data=core;core',            # inclure dossier core
    '--icon=assets/icon.ico',           # icône de l'application
    '--hidden-import=openpyxl'
])