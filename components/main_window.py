import os
import sys

from PySide6 import QtCore
from PySide6.QtGui import QPixmap, QPalette, Qt
from PySide6.QtWidgets import QMainWindow, QMenuBar, QFileDialog, QScrollArea, QLabel


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Imgor")
        self.setMinimumSize(550, 550)

        self.create_menus()

        scroll_area = QScrollArea()
        self.label = QLabel()
        self.label.setBackgroundRole(QPalette.Base)

        scroll_area.setWidget(self.label)
        scroll_area.setAlignment(Qt.AlignCenter)
        self.setCentralWidget(scroll_area)

    def create_menus(self):
        menubar = QMenuBar()
        file_menu = menubar.addMenu("&File")
        file_menu.addAction("&Open...", self.load_image)
        file_menu.addSeparator()
        file_menu.addAction("&Exit", self.exit_app)

        self.setMenuBar(menubar)

    def exit_app(self):
        sys.exit(self.exit_app)

    def load_image(self):
        filename, ok = QFileDialog.getOpenFileName(
            self,
            "Select an Image",
            os.path.join(QtCore.QDir.homePath(), "pictures"),
            "Images (*.png *.jpg *.jpeg)",
        )

        if ok and filename is not None:
            pixmap = QPixmap(filename)
            self.label.setPixmap(pixmap)
            self.label.adjustSize()
