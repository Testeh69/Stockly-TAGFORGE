!["logo stockly tag-forge"](assets\logo.png)


# StocklyTagForgeApp

**Desktop application** pour la génération et l'impression de QR codes destinés à l’application Stockly.

---

## 🚀 Fonctionnalités principales

* **Génération de QR codes** à partir de données de stock (référence, désignation, lot, quantité, etc.)
* **Impression directe** des étiquettes QR via une imprimante configurée sur le système
* **Interface graphique conviviale** basée sur Qt (PyQt6) avec menus, barres d’outils et zone d’aperçu
* **Export** des QR codes en image (PNG/SVG) pour usages externes
* **Configuration personnalisable** : mise en page, taille des étiquettes, marges, police

---

## ⚙️ Prérequis

* **Python 3.9+**
* **PyQt6**: interface graphique
* **qrcode** : génération de QR codes
* **Pillow** : manipulation d’images
* **reportlab** : création et mise en page PDF pour impression
* **pip** (gestionnaire de paquets Python)

---

## 📥 Installation

1. Clonez le dépôt :

   ```bash
   git clone https://github.com/Testeh69/StocklyTagForgeApp.git
   cd StocklyTagForgeApp
   ```
2. Créez et activez un environnement virtuel (optionnel mais recommandé) :

   ```bash
   python -m venv venv
   source venv/bin/activate     # macOS / Linux
   venv\\Scripts\\activate    # Windows
   ```
3. Installez les dépendances :

   ```bash
   pip install -r requirements.txt
   ```

---

## ▶️ Utilisation

1. Lancez l’application :

   ```bash
   python main.py
   ```
2. Dans le menu **Fichier > Importer**, chargez un fichier CSV ou saisissez manuellement les données de stock.
3. Ajustez les paramètres d’impression dans **Paramètres > Mise en page** :

   * Dimensions de l’étiquette
   * Marges
   * Police et taille
4. Cliquez sur **Générer** pour afficher les QR codes en aperçu.
5. Utilisez **Imprimer** pour envoyer les étiquettes à votre imprimante.

---

## 🔧 Personnalisation

* **templates/** : modèles de mise en page PDF (format, orientation)
* **config.json** : paramètres par défaut (taille, police, chemin imprimante)
* **assets/** : icônes et ressources graphiques

---

## 🛠️ Architecture

```
StocklyTagForgeApp/
├── main.py             # Point d'entrée de l'application
├── ui/                 # Fichiers UI (Qt Designer .ui)
├── controllers/        # Logique métier et gestion des actions
├── models/             # Classes de données (StockItem, Settings)
├── templates/          # Modèles PDF pour l'impression
├── assets/             # Icônes et images
├── config.json         # Configuration par défaut
└── requirements.txt    # Dépendances Python
```

---

## 🤝 Contributions

Les contributions sont les bienvenues ! Merci de :

1. Forker ce dépôt
2. Créer une branche (`git checkout -b feature/ma-fonctionnalite`)
3. Committer vos changements (`git commit -m 'Ajout d\`une fonctionnalité'\`)
4. Pousser la branche (`git push origin feature/ma-fonctionnalite`)
5. Ouvrir une Pull Request

---

## 📄 Licence

Ce projet est distribué sous la licence MIT. Voir le fichier [LICENSE](LICENSE) pour plus de détails.

---

*StocklyTagForgeApp* – Simplifiez la gestion et l'étiquetage de votre stock avec des QR codes professionnels !
