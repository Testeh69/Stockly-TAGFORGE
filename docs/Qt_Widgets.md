# 🧱 Widgets on PyQT6

## 1️⃣ Context
**QWidgets** is the main block use to build the components who will be displayed in the window like:

    - a button

    - a menu
    
    - a label
    
    - a set of button, menu, label all together
    
    - and so on


> #### Note
>While QWidget is the base class, PyQt provides specialized widget subclasses for common elements:
>For example, buttons like labels are created using their own class QPushButton class and QLabel class, not QWidget directly.

## 2️⃣ Best Practices for Building a Widgets

The recommended approach is to create a custom class that inherits from QWidgets. This allows you to use all built-in methods provided by the Qt framework.


### 🧱 Basic Structure
```python

from PyQt6.QtWidgets import QWidgets

class MainWigets(QMWidgets):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setGeometry(100, 100, 800, 600)
        self.setMinimumSize(500, 200)

```
## 🔧 Key Methods


### 🖼️ Window Management
| Method                     | Description                                                    |
| -------------------------- | -------------------------------------------------------------- |
| `.setWindowTitle(str)`     | Sets the title of the window                                   |
| `.setGeometry(x, y, w, h)` | Sets the position and size of the widget (x, y, width, height) |
| `.resize(width, height)`   | Resizes the widget to a fixed size                             |
| `.move(x, y)`              | Moves the widget to a specific position on the screen          |
| `.show()`                  | Displays the widget                                            |
| `.hide()`                  | Hides the widget                                               |
| `.close()`                 | Closes the widget                                              |

### 📐 Layout & Appearance


| Method                             | Description                                                        |
| ---------------------------------- | ------------------------------------------------------------------ |
| `.setLayout(layout)`               | Applies a layout (like `QVBoxLayout`, `QHBoxLayout`) to the widget |
| `.setStyleSheet("css-like")`       | Applies a CSS-like style to the widget                             |
| `.setFixedSize(w, h)`              | Fixes the widget size (no resizing allowed)                        |
| `.setMinimumSize(w, h)`            | Sets the minimum size of the widget                                |
| `.setMaximumSize(w, h)`            | Sets the maximum size of the widget                                |
| `.setSizePolicy(policyX, policyY)` | Sets how the widget should grow/shrink                             |

### 🧠 Behavior & Properties

| Method                      | Description                                                  |
| ----------------------------| ------------------------------------------------------------ |
| `.isVisible()`              | Returns `True` if the widget is currently visible            |
| `.setEnabled(True/False)`   | Enables or disables interaction with the widget              |
| `.setToolTip(str)`          | Sets a small tooltip when hovering the mouse over the widget |
| `.setFocus()`               | Gives the widget keyboard focus                              |
| `.update()`                 | Forces a repaint of the widget                               |
| `.repaint()`                | Immediately repaints the widget (used rarely)                |
| `.setAcceptDrop(True/False)`| Accept drop file element                                     |

> Note
>Any widget derived from QWidget is fundamentally a visual container — it can hold content, layout elements, or even other widgets.

## 🧪 Example: Creating and Launching a Main Window with a simple widget


To display widgets inside a QMainWindow, we follow a structured approach. We'll define a helper method that sets up the widgets and layouts, and call this method inside the __init__ method of the MainWindow class.

Within this method:

We create an instance of a custom QWidget that holds our layout and child widgets.

Then, we use **self.setCentralWidget(widget)** to assign it to the main window.

#### 🔧 Steps to Display Widgets in a Widget
If you want to embed widgets inside a widget (e.g., buttons, labels inside a panel), follow this order:

1 Create a layout (e.g., QVBoxLayout, QHBoxLayout, etc.)

2 Create your widgets (e.g., QPushButton, QLabel)

3 Add widgets to the layout using layout.addWidget(widget)

4 Set the layout on the parent widget using parent_widget.setLayout(layout)

```python

from PyQt6.QtWidgets import QWidget, QHBoxLayout, QLabel, QMainWindow, QApplication
from PyQt6.QtCore import Qt
import sys



class mainWindow(QMainWindow):

    def __init__(self, parent = None):
        super().__init__(parent)
        self.setWindowTitle("Test")
        self.setGeometry(100, 100, 800, 600)
        self.setMinimumSize(500, 200)
        self.init_ui()

    def init_ui(self):
        ss = SimpleWidget()
        self.setCentralWidget(ss)



class SimpleWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Simple Widget")
        self.setGeometry(100, 100, 400, 300)

        layout = QHBoxLayout()
        label = QLabel("This is a simple widget", self)
        label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(label)

        self.setLayout(layout)




if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = mainWindow()
    window.show()
    sys.exit(app.exec())



```
### 🖼️ Example Output (UI Screenshot)
<div align="center"> 
<img src="assets_docs\Qt_Widgets.png" alt="Qt Main Window Example" width="600"> 
</div>





> ## Notes
> [Qt Widgets](https://doc.qt.io/qtforpython-6/PySide6/QtWidgets/QWidget.html)