import os.path

from PySide6.QtWidgets import QApplication

from components import MainWindow

if __name__ == "__main__":
    """This is the entry point of the application"""
    app = QApplication([])

    # Load stylesheet
    with open(os.path.join(os.path.dirname(__file__), "styles", "index.qss"), "r") as f:
        stylesheet = f.read()
        app.setStyleSheet(stylesheet)

    window = MainWindow()
    window.show()
    app.exec()
