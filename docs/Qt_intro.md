# **PyQT Introduction**


Below is the basic script that can be use as enter point of the program


```python

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = mainWindow() # or other Class created using inherited QtMainWindow
    window.show()
    sys.exit(app.exec())


```

**QApplication(sys.argv)** : initizialize QT, prepare the env for the IHM and open the event loop.



**window.show()** or **(object__name).show()**:show is a method of the QtMainWindow to show the window.


**sys.exit((app__name).exec())**: is to gere the event and the closing of the app 


**Next**:
# [!Learn About QtMainWidow](docs\Qt_MainWindow.md)