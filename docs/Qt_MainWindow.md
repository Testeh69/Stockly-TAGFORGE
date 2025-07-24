# 🪟 Main Window in PyQt6

## 1️⃣ Context
**QMainWindow** is the foundational class used to build the main window of a PyQt6 application. It provides a robust framework that supports:

    - Menus

    - Toolbars

    - Status bars

    - Dock widgets

    - Central widgets

    - All interface and widget elements (e.g., buttons, charts, tables) are placed inside this main window.

## 2️⃣ Best Practices for Building a Main Window

The recommended approach is to create a custom class that inherits from QMainWindow. This allows you to use all built-in methods provided by the Qt framework.

### 🧱 Basic Structure
```python

from PyQt6.QtWidgets import QMainWindow

class MainWindow(QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("My Application")
        self.setGeometry(100, 100, 800, 600)
        self.setMinimumSize(500, 200)

```
## 🔧 Key Methods


**setWindowTitle(str)** : 	Sets the title of the window (displayed in the title bar)
**setGeometry(x, y, width, height)**:	Defines the initial screen position and dimensions of the window
**setMinimumSize(width, height)**:	Sets the minimum size the window can be resized to

## 💡 Geometry defines where and how big the window is when it launches, not the final resizable bounds.

### 🧪 Example: Creating and Launching a Main Window


```python

import sys
from PyQt6.QtWidgets import QMainWindow, QApplication

class MainWindow(QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Test Application")
        self.setGeometry(100, 100, 800, 600)
        self.setMinimumSize(500, 200)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())


```
### 🖼️ Example Output (UI Screenshot)
<div align="center"> 
<img src="docs/Qt_MainWindow.png" alt="Qt Main Window Example" width="600"> 
</div>
