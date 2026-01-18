"""This module contains the MainWindow class which is an extension of QMainWindow"""

import os
import sys
import platform

from PIL import Image
from PySide6 import QtCore
from PySide6.QtGui import QPixmap, Qt, QImage
from PySide6.QtWidgets import QMainWindow, QMenuBar, QFileDialog, QScrollArea

from components.draggable_label import DraggableLabel


class MainWindow(QMainWindow):
    """The MainWindow class initializes the main window and contains controllers for
    some window actions"""

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Imgor")
        self.setMinimumSize(550, 550)

        self.original_image = None
        self.new_image = None
        self.create_menus()

        scroll_area = QScrollArea()
        scroll_area.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.label = DraggableLabel(scroll_area)

        scroll_area.setWidget(self.label)
        self.setCentralWidget(scroll_area)

    def create_menus(self):
        """This method initializes the application's menu"""
        menubar = QMenuBar()
        file_menu = menubar.addMenu("&File")
        file_menu.addAction("&Open...", self.load_image)
        file_menu.addSeparator()
        file_menu.addAction("&Exit", self.exit_app)

        image_menu = menubar.addMenu("&Image")
        modes_submenu = image_menu.addMenu("&Modes")
        modes_submenu.addAction("&Grayscale", self.convert_to_grayscale)

        self.setMenuBar(menubar)

    def exit_app(self):
        """This method terminates the application"""
        sys.exit(str(self.exit_app))

    def load_image(self):
        """Responsible for loading an image.
        The read image is first converted to "RGBA" before displaying it.
        This fixes a bug where we could not load a grayscale image.
        """
        filename, ok = QFileDialog.getOpenFileName(
            self,
            "Select an Image",
            os.path.join(
                QtCore.QDir.homePath(),
                "pictures" if platform.system() == "Windows" else "Pictures",
            ),
            "Images (*.png *.jpg *.jpeg)",
        )

        if ok and filename is not None:
            # Load the image with PIL and then create a QImage instance
            with Image.open(filename) as img:
                self.original_image = img.convert("RGBA")
                q_image = QImage(
                    self.original_image.tobytes("raw", "RGBA"),
                    self.original_image.width,
                    self.original_image.height,
                    QImage.Format.Format_RGBA8888,
                )
                self.label.setPixmap(QPixmap.fromImage(q_image))
            self.label.adjustSize()

    def convert_to_grayscale(self):
        "This method converts an RGBA image to grayscale"
        if self.original_image is not None:
            self.new_image = self.original_image.convert("L")
            q_image = QImage(
                self.new_image.tobytes("raw", "L"),
                self.new_image.width,
                self.new_image.height,
                self.new_image.width,
                QImage.Format.Format_Grayscale8,
            )
            self.label.setPixmap(QPixmap.fromImage(q_image))
