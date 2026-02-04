"""This module contains the MainWindow class which is an extension of QMainWindow"""

import os
import platform
import sys
import traceback

from PIL import Image
from PIL import ImageFilter
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
        self.is_grayscale = False
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
        file_menu.addAction("&Save as...", self.save_image_as)
        file_menu.addSeparator()
        file_menu.addAction("&Exit", self.exit_app)

        image_menu = menubar.addMenu("&Image")
        rotation_submenu = image_menu.addMenu("&Rotation")
        rotation_submenu.addAction("Reset", self.reset_image_rotation)
        rotation_submenu.addAction("Rotate left", self.rotate_image_left)
        rotation_submenu.addAction("Rotate right", self.rotate_image_right)
        rotation_submenu.addAction(
            "Flip image (Left - Right)", self.flip_image_left_right
        )
        rotation_submenu.addAction(
            "Flip image (Top - Bottom)", self.flip_image_top_bottom
        )
        modes_submenu = image_menu.addMenu("&Modes")
        modes_submenu.addAction("&Grayscale", self.convert_to_grayscale)
        modes_submenu.addAction("&Gaussian Blur", self.apply_gaussian_blur)

        self.setMenuBar(menubar)

    def exit_app(self):
        """This method terminates the application"""
        sys.exit(str(self.exit_app))

    def load_image(self):
        """Responsible for loading an image.
        The read image is first converted to "RGBA" before displaying it.
        This fixes a bug where we could not load a grayscale image.
        """
        self.original_image = None
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

    def save_image_as(self):
        """This method saves an edited image.
        The edited image can have the extensions .png, .jpg or .jpeg
        """
        filename, selected_filter = QFileDialog.getSaveFileName(
            self,
            "Save image as...",
            os.path.join(
                QtCore.QDir.homePath(),
                "pictures" if platform.system() == "Windows" else "Pictures",
            ),
            "PNG (*.png);;JPG (*.jpg);;JPEG (*.jpeg))",
        )

        try:
            if self.new_image is None:
                self.new_image = self.original_image

            # Get the file extension (.png, .jpg, .jpeg)
            extension = selected_filter.split("*")[-1].strip(")")

            if not filename.endswith(extension):
                filename += extension

            if extension == ".jpg" or extension == ".jpeg":
                # We cannot save a jpg or jpeg image with RGBA
                self.new_image = self.new_image.convert("RGB")

            self.new_image.save(filename)
        except (AttributeError, KeyError):
            print(traceback.format_exc())

    def convert_to_grayscale(self):
        """This method converts an RGBA image to grayscale"""
        if self.original_image is not None:
            self.new_image = self.original_image.convert("L")
            self.is_grayscale = True
            q_image = QImage(
                self.new_image.tobytes("raw", "L"),
                self.new_image.width,
                self.new_image.height,
                self.new_image.width,
                QImage.Format.Format_Grayscale8,
            )
            self.label.setPixmap(QPixmap.fromImage(q_image))

    def apply_gaussian_blur(self):
        """apply gaussian blur to the image"""
        if self.original_image is not None:
            img1 = self.original_image.convert("RGBA")
            self.new_image = img1.filter(ImageFilter.GaussianBlur(2))
            q_image = QImage(
                self.new_image.tobytes("raw", "RGBA"),
                self.new_image.width,
                self.new_image.height,
                self.new_image.width * 4,  # ήθελε Χ4 γτ 4 bytes per pixel !!!
                QImage.Format.Format_RGBA8888,
            )
            self.label.setPixmap(QPixmap.fromImage(q_image))

    # TODO: add a utils file that contains file type conversions from and to QT components

    def reset_image_rotation(self):
        raise NotImplementedError

    def rotate_image_left(self):
        try:
            if self.new_image is None:
                self.new_image = self.original_image

            self.new_image = self.new_image.rotate(90, expand=True)
            q_image = QImage(
                self.new_image.tobytes("raw", "RGBA" if not self.is_grayscale else "L"),
                self.new_image.width,
                self.new_image.height,
                (
                    self.new_image.width * 4
                    if not self.is_grayscale
                    else self.new_image.width
                ),
                (
                    QImage.Format.Format_RGBA8888
                    if not self.is_grayscale
                    else QImage.Format.Format_Grayscale8
                ),
            ).copy()

            self.label.setPixmap(QPixmap.fromImage(q_image))
            self.label.resize(self.label.pixmap().size())
        except AttributeError:
            print(traceback.format_exc())

    def rotate_image_right(self):
        try:
            if self.new_image is None:
                self.new_image = self.original_image

            self.new_image = self.new_image.rotate(-90, expand=True)
            q_image = QImage(
                self.new_image.tobytes("raw", "RGBA" if not self.is_grayscale else "L"),
                self.new_image.width,
                self.new_image.height,
                (
                    self.new_image.width * 4
                    if not self.is_grayscale
                    else self.new_image.width
                ),
                (
                    QImage.Format.Format_RGBA8888
                    if not self.is_grayscale
                    else QImage.Format.Format_Grayscale8
                ),
            ).copy()

            self.label.setPixmap(QPixmap.fromImage(q_image))
            self.label.resize(self.label.pixmap().size())
        except AttributeError:
            print(traceback.format_exc())

    def flip_image_left_right(self):
        try:
            if self.new_image is None:
                self.new_image = self.original_image

            self.new_image = self.new_image.transpose(Image.Transpose.FLIP_LEFT_RIGHT)
            q_image = QImage(
                self.new_image.tobytes("raw", "RGBA" if not self.is_grayscale else "L"),
                self.new_image.width,
                self.new_image.height,
                (
                    self.new_image.width * 4
                    if not self.is_grayscale
                    else self.new_image.width
                ),
                (
                    QImage.Format.Format_RGBA8888
                    if not self.is_grayscale
                    else QImage.Format.Format_Grayscale8
                ),
            ).copy()

            self.label.setPixmap(QPixmap.fromImage(q_image))
            self.label.resize(self.label.pixmap().size())
        except AttributeError:
            print(traceback.format_exc())

    def flip_image_top_bottom(self):
        try:
            if self.new_image is None:
                self.new_image = self.original_image

            self.new_image = self.new_image.transpose(Image.Transpose.FLIP_TOP_BOTTOM)
            q_image = QImage(
                self.new_image.tobytes("raw", "RGBA" if not self.is_grayscale else "L"),
                self.new_image.width,
                self.new_image.height,
                (
                    self.new_image.width * 4
                    if not self.is_grayscale
                    else self.new_image.width
                ),
                (
                    QImage.Format.Format_RGBA8888
                    if not self.is_grayscale
                    else QImage.Format.Format_Grayscale8
                ),
            ).copy()

            self.label.setPixmap(QPixmap.fromImage(q_image))
            self.label.resize(self.label.pixmap().size())
        except AttributeError:
            print(traceback.format_exc())
