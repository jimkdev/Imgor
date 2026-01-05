import os
import sys

from PySide6 import QtCore
from PySide6.QtGui import QPixmap, Qt
from PySide6.QtWidgets import QMainWindow, QMenuBar, QFileDialog, QScrollArea

from components.draggable_label import DraggableLabel


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Imgor")
        self.setMinimumSize(550, 550)

        self.create_menus()

        scroll_area = QScrollArea()
        scroll_area.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.label = DraggableLabel(scroll_area)

        scroll_area.setWidget(self.label)
        self.setCentralWidget(scroll_area)

    def create_menus(self):
        menubar = QMenuBar()
        file_menu = menubar.addMenu("&File")
        file_menu.addAction("&Open...", self.load_image)
        file_menu.addSeparator()
        file_menu.addAction("&Exit", self.exit_app)

        self.setMenuBar(menubar)

    def exit_app(self):
        sys.exit(str(self.exit_app))

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
