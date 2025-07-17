# Qt_Doc


## Introduction

Personnal documentation based on the problem that i have meet while building this desktop app.


___

Q_Widget : class imported to build widget 

Un layout est un objet qui sert à organiser automatiquement la disposition des widgets (boutons, labels, champs, etc.) dans une fenêtre ou un conteneur.

QVBoxLayout est un layout vertical

```python
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QPushButton

class MaFenetre(QWidget):
    def __init__(self):
        super().__init__()

        layout = QVBoxLayout()  # création d’un layout vertical

        btn1 = QPushButton("Bouton 1")
        btn2 = QPushButton("Bouton 2")
        btn3 = QPushButton("Bouton 3")

        # Ajouter les boutons au layout
        layout.addWidget(btn1)
        layout.addWidget(btn2)
        layout.addWidget(btn3)

        # Assigner le layout au widget principal
        self.setLayout(layout)
```


QLayout n'a pas de méthode title, dimension contrairement au QWidget