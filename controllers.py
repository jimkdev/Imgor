from PIL import Image
from PySide6.QtGui import QImage

from enums import ImageFlipOrientations


def create_q_image(image, is_grayscale):
    return QImage(
                image.tobytes("raw", "RGBA" if not is_grayscale else "L"),
                image.width,
                image.height,
                (
                    image.width * 4
                    if not is_grayscale
                    else image.width
                ),
                (
                    QImage.Format.Format_RGBA8888
                    if not is_grayscale
                    else QImage.Format.Format_Grayscale8
                ),
            ).copy()


def flip_image(image, choice):
    if choice == ImageFlipOrientations.TOP_BOTTOM.value:
        return image.transpose(Image.Transpose.FLIP_TOP_BOTTOM)

    if choice == ImageFlipOrientations.LEFT_RIGHT.value:
        return image.transpose(Image.Transpose.FLIP_LEFT_RIGHT)

    return None
